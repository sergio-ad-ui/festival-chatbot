#!/usr/bin/env python3
"""
Script per generare un token WhatsApp di lunga durata (60 giorni)
Alternativa al token permanente quando ci sono problemi di approvazione
"""

import requests
import json

def generate_long_lived_token():
    """
    Genera un token di lunga durata per WhatsApp Business API
    """
    print("🔑 GENERAZIONE TOKEN WHATSAPP LUNGA DURATA")
    print("=" * 50)
    
    # Token temporaneo attuale (quello che scade in 24h)
    short_lived_token = input("📱 Inserisci il tuo TOKEN TEMPORANEO attuale: ")
    app_id = input("📲 Inserisci l'APP ID della tua app Facebook: ")
    app_secret = input("🔐 Inserisci l'APP SECRET della tua app: ")
    
    if not all([short_lived_token, app_id, app_secret]):
        print("❌ Tutti i campi sono obbligatori!")
        return
    
    # URL per estendere il token
    url = "https://graph.facebook.com/v17.0/oauth/access_token"
    
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token
    }
    
    try:
        print("\n🚀 Richiesta token di lunga durata...")
        response = requests.get(url, params=params)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            long_lived_token = data.get("access_token")
            expires_in = data.get("expires_in", "Unknown")
            
            print("\n✅ TOKEN DI LUNGA DURATA GENERATO!")
            print("-" * 40)
            print(f"🔑 Token: {long_lived_token}")
            print(f"⏰ Scade in: {expires_in} secondi (~60 giorni)")
            print("\n💡 Copia questo token e usalo su Render!")
            
            return long_lived_token
        else:
            print(f"❌ Errore nella generazione: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return None

def where_to_find_app_details():
    """
    Guida per trovare App ID e Secret
    """
    print("\n📋 DOVE TROVARE APP ID E SECRET")
    print("-" * 40)
    print("1. Vai su https://developers.facebook.com/apps/")
    print("2. Seleziona la tua app WhatsApp")
    print("3. Vai su 'App Settings' > 'Basic'")
    print("4. App ID: visibile in alto")
    print("5. App Secret: clicca 'Show' accanto a 'App Secret'")
    print("\n📱 Token temporaneo: lo trovi nella dashboard WhatsApp della tua app")

if __name__ == "__main__":
    print("🎯 Hai 2 opzioni:")
    print("1. Genera token di lunga durata (60 giorni)")
    print("2. Mostra dove trovare App ID e Secret")
    
    choice = input("\nScegli opzione (1 o 2): ")
    
    if choice == "1":
        generate_long_lived_token()
    elif choice == "2":
        where_to_find_app_details()
    else:
        print("Opzione non valida!") 