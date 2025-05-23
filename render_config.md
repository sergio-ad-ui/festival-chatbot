# 🚀 CONFIGURAZIONE RENDER - TOKEN TEMPORANEO

## ⚙️ Variabili d'Ambiente per Render

```env
# WhatsApp Configuration (Token Temporaneo - 24h)
WHATSAPP_API_TOKEN=EAFWKr4T33p4BO8P78HpWqTReab2hVzkYcFlOQ9oZAgU9lIpuZAVWQmH4xDY9Ng5E3MQrge20cxfwsDYmfadqasgdEFhFzGkzfewRMZBPyVoOQst4t1ZCvpeNAhi17Ufr3tmPiVNZA4FgOlHjON7MyaZC8jZBbis8lZCWh0XBZCMYFLJuWeSlv4sC6dnqaWcZCMhFD2oRuq9qAVpYXyR4wiFs335WswEgR9woS6hGsZD
PHONE_NUMBER_ID=693374467190125
WHATSAPP_PHONE_NUMBER=+34644409180
VERIFY_TOKEN=festival_bot_verify_token

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MongoDB Configuration  
MONGODB_URI=your_mongodb_connection_string_here
MONGODB_DB_NAME=festival_chatbot

# App Configuration
DEBUG=False
PORT=5000
CONVERSATION_EXPIRES_MINS=60
MAX_TOKENS=500
```

## 🎯 Status Attuale

✅ **Token Temporaneo**: Funziona perfettamente (24 ore)
✅ **Numero WhatsApp**: +34 644 40 91 80 attivo  
✅ **Display Name**: "Appartamento Smeraldo" approvato
⏳ **Token Permanente**: In attesa autorizzazioni aggiuntive

## 📋 Prossimi Passi

1. **Immediate**: Aggiorna Render con configurazione sopra
2. **24h**: Setup UptimeRobot per keep-alive gratuito
3. **Future**: Passa al token permanente quando pronto

## 🔄 Rinnovo Token (24h)

Quando il token temporaneo scade:
1. Vai su developers.facebook.com
2. Genera nuovo "Token di accesso temporaneo"
3. Aggiorna WHATSAPP_API_TOKEN su Render

## 💎 Token Permanente (Futuro)

Quando avrai l'autorizzazione aggiuntiva:
1. Usa `scripts/generate_new_permanent_token.py`
2. Sostituisci WHATSAPP_API_TOKEN
3. Zero manutenzione futura! 