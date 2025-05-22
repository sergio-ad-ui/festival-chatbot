# Configurare l'App su Render.com

Ecco una guida passo-passo per deployare questa applicazione su Render.com:

## 1. Prepara il tuo repository GitHub

1. Crea un nuovo repository su GitHub
2. Assicurati che il file `.env` sia nel `.gitignore`
3. Esegui questi comandi:

```bash
git init
git add .
git commit -m "Primo commit"
git branch -M main
git remote add origin https://github.com/username/nome-repository.git
git push -u origin main
```

## 2. Connetti Render a GitHub

1. Vai su [render.com](https://render.com/) e crea un account o accedi
2. Vai su "New" e seleziona "Web Service"
3. Connetti il tuo account GitHub
4. Seleziona il repository che hai appena creato

## 3. Configura il Web Service su Render

1. Dai un nome al tuo servizio (es. "festival-chatbot")
2. Seleziona "Docker" come runtime
3. Mantieni il ramo "main" come predefinito
4. Nella sezione "Advanced", aggiungi tutte le variabili d'ambiente dal tuo file `.env`:

```
OPENAI_API_KEY=la_tua_chiave_openai
WHATSAPP_API_TOKEN=il_tuo_token_whatsapp
WHATSAPP_PHONE_NUMBER_ID=il_tuo_phone_number_id
VERIFY_TOKEN=il_tuo_token_di_verifica
MONGODB_URI=il_tuo_mongodb_uri
MONGODB_DB_NAME=festival_db
```

5. Per il database MongoDB, consigliamo di utilizzare MongoDB Atlas, che offre un livello gratuito. Assicurati di aggiornare `MONGODB_URI` con l'URI corretto del tuo database.

6. Clicca su "Create Web Service"

## 4. Configura il Webhook WhatsApp

Dopo che Render ha deployato la tua app:

1. Copia l'URL del tuo servizio Render (sarà qualcosa come `https://festival-chatbot.onrender.com`)
2. Vai su [developers.facebook.com](https://developers.facebook.com/) e accedi alla tua app
3. Nella dashboard dell'app, vai su "WhatsApp" → "Configurazione"
4. Nella sezione "Webhook", aggiungi un nuovo webhook
5. Imposta l'URL come `https://festival-chatbot.onrender.com/webhook`
6. Imposta il token di verifica con lo stesso valore che hai inserito per `VERIFY_TOKEN` nelle variabili d'ambiente di Render
7. Seleziona gli eventi che vuoi ricevere (almeno "messages")
8. Salva la configurazione

## 5. Testa il tuo Chatbot

1. Invia un messaggio al numero WhatsApp che hai configurato
2. Verifica i log su Render per assicurarti che tutto funzioni correttamente
3. Il tuo chatbot dovrebbe rispondere al messaggio!

## Risoluzione dei problemi

Se riscontri problemi:

1. Controlla i log su Render per eventuali errori
2. Verifica che tutte le variabili d'ambiente siano configurate correttamente
3. Assicurati che il webhook WhatsApp sia configurato con l'URL e il token corretti
4. Controlla che MongoDB sia accessibile dalla tua app (se usi MongoDB Atlas, assicurati di aver aggiunto l'IP di Render alla lista degli IP consentiti)

Per qualsiasi altra domanda, consulta la documentazione di [Render](https://render.com/docs) o [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/cloud-api). 