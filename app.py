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

# Carica le variabili d'ambiente
load_dotenv()

app = Flask(__name__)

# Configurazione OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurazione MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DB_NAME")]
conversations_collection = db["conversations"]
festival_info_collection = db["festival_info"]

# Configurazione WhatsApp API
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

WHATSAPP_HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json"
}

# Durata massima di una conversazione in minuti
CONVERSATION_EXPIRES_MINS = int(os.getenv("CONVERSATION_EXPIRES_MINS", 60))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))

@app.route("/", methods=["GET"])
def index():
    return "Chatbot del Festival attivo!"

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
    
    # Ottieni o crea la conversazione
    conversation = get_or_create_conversation(sender_id)
    
    # Aggiungi il messaggio alla conversazione
    conversation["messages"].append({
        "role": "user",
        "content": message_text,
        "timestamp": datetime.now()
    })
    
    # Ottieni risposta dall'AI
    print(f"Generazione risposta AI per {sender_id}")
    ai_response = generate_ai_response(conversation)
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

def get_or_create_conversation(sender_id):
    # Cerca una conversazione esistente non scaduta
    expiry_time = datetime.now() - timedelta(minutes=CONVERSATION_EXPIRES_MINS)
    conversation = conversations_collection.find_one({
        "sender_id": sender_id,
        "last_updated": {"$gt": expiry_time}
    })
    
    if conversation:
        return conversation
    
    # Crea una nuova conversazione
    new_conversation = {
        "sender_id": sender_id,
        "messages": [],
        "created_at": datetime.now(),
        "last_updated": datetime.now()
    }
    
    result = conversations_collection.insert_one(new_conversation)
    new_conversation["_id"] = result.inserted_id
    
    return new_conversation

def generate_ai_response(conversation):
    # Prepara il contesto con le informazioni sul festival
    system_message = get_festival_context()
    
    # Prepara i messaggi per l'API di OpenAI
    messages = [{"role": "system", "content": system_message}]
    
    # Aggiungi gli ultimi messaggi della conversazione
    # Limitiamo a un numero ragionevole per non superare il contesto massimo
    recent_messages = conversation["messages"][-10:]
    for msg in recent_messages:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        # Chiamata all'API di OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Errore nell'API OpenAI: {e}")
        return "Mi dispiace, si è verificato un errore. Riprova più tardi."

def get_festival_context():
    # Recupera tutte le informazioni sul festival dal database
    festival_info = list(festival_info_collection.find())
    
    # Crea un contesto informativo per l'AI
    context = "Sei un assistente virtuale per un festival. "
    context += "Il tuo compito è fornire informazioni accurate sull'evento, aiutare con le direzioni, "
    context += "spiegare gli orari e rispondere a domande sui servizi disponibili. "
    context += "Ecco le informazioni sul festival:\n\n"
    
    # Aggiungi le informazioni specifiche dal database
    for info in festival_info:
        if "category" in info and "content" in info:
            context += f"{info['category']}: {info['content']}\n"
    
    return context

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

# Registra le route del pannello di amministrazione
register_admin_routes(app)

# Le route di amministrazione sono ora gestite dal modulo admin_panel

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug) 