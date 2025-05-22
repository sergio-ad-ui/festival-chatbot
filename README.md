# Chatbot WhatsApp per Festival

Un'applicazione che collega WhatsApp con l'API di OpenAI per creare un chatbot intelligente per il tuo festival. Il chatbot può fornire informazioni sull'evento, orari, mappe e rispondere alle domande dei partecipanti.

## Caratteristiche

- Integrazione diretta con l'API WhatsApp di Meta (senza Twilio)
- Utilizzo dell'API di OpenAI per generare risposte intelligenti
- Database MongoDB per memorizzare le conversazioni e le informazioni del festival
- Pannello di amministrazione per gestire le informazioni sul festival
- Pronto per il deployment su render.com

## Prerequisiti

- Account WhatsApp Business Platform
- API key di OpenAI
- Database MongoDB (puoi usare MongoDB Atlas per un database cloud gratuito)

## Setup

1. Clona questo repository
2. Crea un file `.env` basato su `.env_example` e compila con le tue API key e configurazioni
3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione in locale:

```bash
python app.py
```

## Configurazione WhatsApp Business API

1. Crea un account [WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
2. Configura un'app Meta for Developers
3. Configura un numero di telefono WhatsApp Business
4. Crea un token di accesso permanente
5. Configura il webhook per puntare all'URL della tua applicazione (es. `https://tua-app.onrender.com/webhook`)
6. Usa lo stesso `VERIFY_TOKEN` nel file `.env` e nella configurazione del webhook

## Configurazione del Database

Il chatbot utilizza MongoDB per memorizzare:

- Conversazioni con gli utenti
- Informazioni sul festival (orari, luoghi, artisti, FAQ)
- Punti sulla mappa dell'evento
- Dettagli degli eventi

Assicurati di creare un database su MongoDB Atlas o su un server MongoDB locale.

## Deployment su Render.com

1. Registrati su [Render](https://render.com/)
2. Crea un nuovo Web Service
3. Collega il tuo repository GitHub
4. Seleziona il branch `main`
5. Imposta il nome del tuo servizio
6. Seleziona "Docker" come runtime
7. Aggiungi le variabili d'ambiente dal tuo file `.env`
8. Clicca su "Create Web Service"

## Pannello di Amministrazione

Il pannello di amministrazione è accessibile all'indirizzo `/admin` e ti permette di:

- Aggiungere/modificare informazioni sul festival
- Gestire gli eventi
- Aggiungere punti sulla mappa
- Visualizzare le statistiche delle conversazioni

## Struttura del Progetto

- `app.py`: Applicazione principale Flask
- `admin_panel.py`: Blueprint Flask per il pannello di amministrazione
- `models.py`: Definizioni dei modelli dati con Pydantic
- `Dockerfile`: Configurazione per il deployment Docker
- `requirements.txt`: Dipendenze Python

## Contribuire

Sentiti libero di contribuire a questo progetto aprendo issue o inviando pull request.

## Licenza

MIT 