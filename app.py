import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import requests
from pymongo import MongoClient
from bson import ObjectId

# Importo il modulo admin_panel
from admin_panel import register_admin_routes
# Importo il nuovo context manager
from context_manager import ContextManager
# Importo il servizio Cloudinary
from cloudinary_service import cloudinary_service

# Carica le variabili d'ambiente
load_dotenv()

app = Flask(__name__)

# Configurazione OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configurazione MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DB_NAME")]
conversations_collection = db["conversations"]
festival_info_collection = db["festival_info"]

# Inizializza il Context Manager
context_manager = ContextManager(db)
# Inizializza i contesti di default se necessario
context_manager.initialize_default_contexts()

# Configurazione WhatsApp API
# IMPORTANTE: Aggiornare il token di accesso WhatsApp nel file .env 
# poiché il token attuale è scaduto (21-May-25)
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

WHATSAPP_HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json"
}

# Durata massima di una conversazione in minuti (ridotta per informazioni aggiornate)
CONVERSATION_EXPIRES_MINS = int(os.getenv("CONVERSATION_EXPIRES_MINS", 30))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))

@app.route("/", methods=["GET"])
def index():
    return "ConnyUp Multi-Context Bot attivo! 🤖"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    # Verifica del webhook da parte di Facebook
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    verify_token = os.getenv("VERIFY_TOKEN", "festival_bot_verify_token")
    
    print(f"Verifica webhook: mode={mode}, token={token}, challenge={challenge}, verify_token={verify_token}")
    
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print(f"Verifica webhook riuscita! Rispondendo con challenge: {challenge}")
            return challenge, 200
        else:
            print(f"Verifica webhook fallita! Token non corrisponde o mode non è 'subscribe'")
            return "Verifica fallita", 403
    
    return "Hello World", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Ricevuto webhook POST: {json.dumps(data)}")
    
    # Verifica se è un messaggio WhatsApp
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    
                    print(f"Ricevuti {len(messages)} messaggi")
                    
                    for message in messages:
                        print(f"Elaborazione messaggio: {json.dumps(message)}")
                        if message.get("type") == "text":
                            handle_text_message(message)
                        # Puoi gestire altri tipi di messaggi qui (immagini, audio, ecc.)
    else:
        print(f"Oggetto webhook non riconosciuto: {data.get('object')}")
    
    return "OK", 200

def handle_text_message(message):
    sender_id = message.get("from")
    message_text = message.get("text", {}).get("body", "")
    
    print(f"Gestione messaggio da {sender_id}: {message_text}")
    
    # Identifica il contesto del messaggio
    context = context_manager.identify_context_from_message(message_text, sender_id)
    print(f"🎯 DEBUG APP: Contesto identificato: '{context}'")
    
    # Se non c'è contesto e l'utente sembra chiedere aiuto, mostra il menu
    if not context and context_manager.should_show_context_menu(message_text):
        menu_message = context_manager.get_context_menu()
        send_whatsapp_message(sender_id, menu_message)
        return
    
    # Ottieni o crea la conversazione con il contesto
    conversation = get_or_create_conversation(sender_id, context)
    
    # Se è un nuovo contesto (codice di avvio), invia il messaggio di benvenuto
    if any(code in message_text.upper() for code in context_manager.START_CODES.keys()):
        welcome_message = context_manager.get_welcome_message(context)
        send_whatsapp_message(sender_id, welcome_message)
        # Aggiungi il messaggio di benvenuto alla conversazione
        conversation["messages"].append({
            "role": "assistant",
            "content": welcome_message,
            "timestamp": datetime.now()
        })
        # Aggiorna la conversazione nel database
        conversations_collection.update_one(
            {"_id": conversation["_id"]},
            {"$set": {"messages": conversation["messages"], "last_updated": datetime.now()}}
        )
        return
    
    # Aggiungi il messaggio alla conversazione
    conversation["messages"].append({
        "role": "user",
        "content": message_text,
        "timestamp": datetime.now()
    })
    
    # Ottieni risposta dall'AI con il contesto appropriato
    print(f"Generazione risposta AI per {sender_id} nel contesto {context}")
    ai_response = generate_ai_response(conversation, context)
    print(f"Risposta AI generata: {ai_response}")
    
    # Aggiungi la risposta dell'AI alla conversazione
    conversation["messages"].append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now()
    })
    
    # Aggiorna la conversazione nel database
    conversations_collection.update_one(
        {"_id": conversation["_id"]},
        {"$set": {"messages": conversation["messages"], "last_updated": datetime.now()}}
    )
    
    # Invia risposta a WhatsApp
    print(f"Invio risposta a {sender_id}: {ai_response}")
    success = send_whatsapp_message(sender_id, ai_response)
    print(f"Risposta inviata con successo: {success}")

def get_or_create_conversation(sender_id, context):
    # Cerca una conversazione esistente non scaduta per questo contesto
    expiry_time = datetime.now() - timedelta(minutes=CONVERSATION_EXPIRES_MINS)
    conversation = conversations_collection.find_one({
        "sender_id": sender_id,
        "context": context,
        "last_updated": {"$gt": expiry_time}
    })
    
    if conversation:
        return conversation
    
    # Crea una nuova conversazione con il contesto
    new_conversation = {
        "sender_id": sender_id,
        "context": context,
        "messages": [],
        "created_at": datetime.now(),
        "last_updated": datetime.now()
    }
    
    result = conversations_collection.insert_one(new_conversation)
    new_conversation["_id"] = result.inserted_id
    
    return new_conversation

def generate_ai_response(conversation, context):
    print(f"🤖 DEBUG APP: Inizio generazione risposta AI per contesto: {context}")
    
    # Ottieni il prompt di sistema appropriato per il contesto
    print(f"🤖 DEBUG APP: Chiamata context_manager.get_context_prompt('{context}')")
    system_message = context_manager.get_context_prompt(context)
    print(f"🤖 DEBUG APP: Prompt ricevuto - lunghezza: {len(system_message)} caratteri")
    print(f"🤖 DEBUG APP: Prompt contenuto: {system_message[:200]}...")
    
    # Verifica se contiene dati dell'admin
    if "dal 15 al 18 giugno 2025" in system_message:
        print("✅ DEBUG APP: PROMPT CONTIENE DATI DELL'ADMIN!")
    else:
        print("❌ DEBUG APP: PROMPT NON CONTIENE DATI DELL'ADMIN!")
    
    # Prepara i messaggi per l'API di OpenAI
    messages = [{"role": "system", "content": system_message}]
    
    # Aggiungi gli ultimi messaggi della conversazione
    # Limitiamo a un numero ragionevole per non superare il contesto massimo
    recent_messages = conversation["messages"][-10:]
    for msg in recent_messages:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    print(f"🤖 DEBUG APP: Invio a OpenAI {len(messages)} messaggi")
    
    try:
        # Chiamata all'API OpenAI aggiornata (versione 1.0+)
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"🤖 DEBUG APP: Risposta OpenAI ricevuta - lunghezza: {len(ai_response)} caratteri")
        
        return ai_response
    except Exception as e:
        print(f"❌ DEBUG APP: Errore nell'API OpenAI: {e}")
        return "Mi dispiace, si è verificato un errore. Riprova più tardi."

def get_festival_context():
    # Questa funzione è mantenuta per compatibilità ma ora usa il context manager
    return context_manager.get_context_prompt("festival")

def send_whatsapp_message(recipient_id, message_text):
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": message_text}
    }
    
    try:
        print(f"Invio messaggio WhatsApp: {json.dumps(payload)}")
        print(f"Headers: {json.dumps(WHATSAPP_HEADERS)}")
        print(f"URL: {WHATSAPP_API_URL}")
        
        response = requests.post(
            WHATSAPP_API_URL,
            headers=WHATSAPP_HEADERS,
            json=payload
        )
        
        print(f"Risposta API WhatsApp: Status {response.status_code}")
        print(f"Risposta API WhatsApp: Body {response.text}")
        
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Errore nell'invio del messaggio WhatsApp: {e}")
        return False

def send_whatsapp_image(recipient_id, image_url, caption=""):
    """
    Invia un'immagine via WhatsApp
    
    Args:
        recipient_id: ID del destinatario
        image_url: URL dell'immagine
        caption: Didascalia opzionale
    """
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }
    
    try:
        print(f"📸 Invio immagine WhatsApp: {image_url}")
        print(f"Caption: {caption}")
        
        response = requests.post(
            WHATSAPP_API_URL,
            headers=WHATSAPP_HEADERS,
            json=payload
        )
        
        print(f"Risposta API WhatsApp (immagine): Status {response.status_code}")
        print(f"Risposta API WhatsApp (immagine): Body {response.text}")
        
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Errore nell'invio dell'immagine WhatsApp: {e}")
        return False

def send_whatsapp_message_with_image(recipient_id, message_text, image_public_id=None, image_caption=""):
    """
    Invia un messaggio con opzionale immagine da Cloudinary
    
    Args:
        recipient_id: ID del destinatario
        message_text: Testo del messaggio
        image_public_id: ID pubblico dell'immagine su Cloudinary (opzionale)
        image_caption: Didascalia dell'immagine (opzionale)
    """
    success = True
    
    # Invia prima il testo
    if message_text:
        success = send_whatsapp_message(recipient_id, message_text)
    
    # Poi invia l'immagine se presente
    if image_public_id and success:
        image_url = cloudinary_service.get_optimized_url(image_public_id, width=800, height=600)
        if image_url:
            success = send_whatsapp_image(recipient_id, image_url, image_caption)
        else:
            print(f"❌ Impossibile ottenere URL per immagine: {image_public_id}")
            success = False
    
    return success

# Registra le route del pannello di amministrazione
register_admin_routes(app)

# Le route di amministrazione sono ora gestite dal modulo admin_panel

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug) 