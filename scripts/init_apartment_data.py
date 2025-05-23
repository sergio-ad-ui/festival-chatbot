"""
Script per inizializzare i dati dell'appartamento di Brescia nel database
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Aggiungi la directory parent al path per importare i moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Connessione al database
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DB_NAME")]

# Collections
apartment_info_collection = db["apartment_info"]
local_services_collection = db["local_services"]
smart_home_collection = db["smart_home_instructions"]

def init_apartment_info():
    """Inizializza le informazioni base dell'appartamento"""
    
    # Pulisci dati esistenti per apt_brescia
    apartment_info_collection.delete_many({"context_code": "apt_brescia"})
    
    apartment_data = [
        {
            "context_code": "apt_brescia",
            "category": "check_in",
            "content": """Il check-in è disponibile dalle 15:00. 
Il check-in è completamente self-service tramite TTLock. 
Ti invierò il codice di accesso via WhatsApp il giorno del tuo arrivo. 
L'appartamento si trova in Via Smeraldo 15, Brescia (3° piano).
Per qualsiasi problema con il check-in, contattami immediatamente.""",
            "priority": 1,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "check_out",
            "content": """Il check-out è entro le 11:00.
Prima di partire, per favore:
- Lascia le chiavi sul tavolo della cucina
- Chiudi tutte le finestre
- Spegni luci e climatizzatore
- Getta la spazzatura nei bidoni in cortile""",
            "priority": 2,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "wifi",
            "content": """WiFi: AppartamentoSmeraldo
Password: Brescia2024!
Velocità: 100 Mbps fibra ottica
Se hai problemi di connessione, riavvia il router (sotto la TV)""",
            "priority": 3,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "regole_casa",
            "content": """Regole della casa:
- No party o eventi
- Rispetta il silenzio dalle 22:00 alle 8:00
- No fumatori (balcone OK)
- Max 4 ospiti
- No animali domestici
- Rispetta i vicini""",
            "priority": 4,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "servizi_inclusi",
            "content": """Servizi inclusi:
- WiFi ultra veloce
- Aria condizionata/riscaldamento
- Lavatrice
- Cucina completamente attrezzata
- Smart TV con Netflix
- Asciugacapelli
- Ferro e asse da stiro
- Set di asciugamani e lenzuola""",
            "priority": 5,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "parcheggio",
            "content": """Parcheggio:
- Parcheggio gratuito in strada con strisce bianche
- Parcheggio a pagamento (strisce blu): €1.20/ora (8:00-20:00)
- Parcheggio coperto più vicino: Garage Centro (5 min a piedi) - €15/giorno
- Domenica parcheggio gratuito ovunque""",
            "priority": 6,
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "category": "emergenze",
            "content": """Numeri di emergenza:
- Emergenza generale: 112
- Proprietario: +39 333 1234567
- Ospedale più vicino: Spedali Civili (10 min auto)
- Farmacia 24h: Farmacia Centrale, Corso Zanardelli""",
            "priority": 10,
            "created_at": datetime.now()
        }
    ]
    
    apartment_info_collection.insert_many(apartment_data)
    print(f"✅ Inserite {len(apartment_data)} informazioni appartamento")

def init_local_services():
    """Inizializza i servizi locali vicino all'appartamento"""
    
    # Pulisci dati esistenti
    local_services_collection.delete_many({"context_code": "apt_brescia"})
    
    services = [
        # Ristoranti
        {
            "context_code": "apt_brescia",
            "type": "restaurant",
            "name": "Osteria Al Bianchi",
            "description": "Cucina tradizionale bresciana, famosa per i casoncelli e lo spiedo",
            "address": "Via Gasparo da Salò 32",
            "distance": "5 minuti a piedi",
            "phone": "+39 030 292328",
            "opening_hours": "12:00-14:30, 19:00-23:00 (Chiuso lunedì)",
            "rating": 4.6,
            "price_range": "€€",
            "google_maps_url": "https://maps.app.goo.gl/example1",
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "type": "restaurant",
            "name": "Pizzeria da Franco",
            "description": "Pizza napoletana autentica, forno a legna",
            "address": "Via San Faustino 48",
            "distance": "8 minuti a piedi",
            "phone": "+39 030 1234567",
            "opening_hours": "12:00-15:00, 18:30-23:30",
            "rating": 4.5,
            "price_range": "€",
            "google_maps_url": "https://maps.app.goo.gl/example2",
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "type": "restaurant",
            "name": "Trattoria della Nonna",
            "description": "Ambiente familiare, ottimi primi piatti fatti in casa",
            "address": "Via Moretto 17",
            "distance": "10 minuti a piedi",
            "rating": 4.4,
            "price_range": "€€",
            "created_at": datetime.now()
        },
        # Supermercati
        {
            "context_code": "apt_brescia",
            "type": "supermarket",
            "name": "Carrefour Express",
            "description": "Supermercato di quartiere, aperto anche la domenica",
            "address": "Via Gramsci 5",
            "distance": "3 minuti a piedi",
            "opening_hours": "8:00-21:00 (Dom 9:00-20:00)",
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "type": "supermarket",
            "name": "Esselunga",
            "description": "Grande supermercato con vasta scelta",
            "address": "Via Triumplina 83",
            "distance": "15 minuti a piedi o 5 in auto",
            "opening_hours": "7:30-22:00",
            "created_at": datetime.now()
        },
        # Farmacie
        {
            "context_code": "apt_brescia",
            "type": "pharmacy",
            "name": "Farmacia San Faustino",
            "description": "Farmacia di quartiere",
            "address": "Via San Faustino 23",
            "distance": "5 minuti a piedi",
            "phone": "+39 030 2400123",
            "opening_hours": "8:30-12:30, 15:30-19:30 (Chiuso domenica)",
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "type": "pharmacy",
            "name": "Farmacia Centrale H24",
            "description": "Farmacia aperta 24 ore su 24",
            "address": "Corso Zanardelli 45",
            "distance": "12 minuti a piedi",
            "phone": "+39 030 291291",
            "opening_hours": "24/7",
            "created_at": datetime.now()
        },
        # Bar/Colazione
        {
            "context_code": "apt_brescia",
            "type": "cafe",
            "name": "Bar Centrale",
            "description": "Ottimi cornetti e cappuccino, terrazza esterna",
            "address": "Piazza della Loggia",
            "distance": "7 minuti a piedi",
            "opening_hours": "7:00-20:00",
            "rating": 4.3,
            "price_range": "€",
            "created_at": datetime.now()
        },
        # Attrazioni
        {
            "context_code": "apt_brescia",
            "type": "attraction",
            "name": "Castello di Brescia",
            "description": "Fortezza medievale con vista panoramica sulla città",
            "address": "Via del Castello",
            "distance": "15 minuti a piedi",
            "opening_hours": "10:00-18:00 (Estate fino alle 19:00)",
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "type": "attraction",
            "name": "Museo di Santa Giulia",
            "description": "Patrimonio UNESCO, storia di Brescia dall'età preistorica",
            "address": "Via Musei 81/b",
            "distance": "10 minuti a piedi",
            "phone": "+39 030 2977833",
            "opening_hours": "Mar-Dom 10:00-18:00",
            "created_at": datetime.now()
        }
    ]
    
    local_services_collection.insert_many(services)
    print(f"✅ Inseriti {len(services)} servizi locali")

def init_smart_home_instructions():
    """Inizializza le istruzioni per i dispositivi smart"""
    
    # Pulisci dati esistenti
    smart_home_collection.delete_many({"context_code": "apt_brescia"})
    
    instructions = [
        {
            "context_code": "apt_brescia",
            "device": "ttlock",
            "title": "Serratura Smart TTLock",
            "instructions": """Per aprire la porta con TTLock:
1. Scarica l'app TTLock dal Play Store/App Store
2. Attiva il Bluetooth
3. Inserisci il codice che ti ho inviato
4. Avvicinati alla porta e premi 'Unlock' nell'app
5. La porta si aprirà automaticamente

Il codice è valido solo per il periodo del tuo soggiorno.""",
            "troubleshooting": [
                "Se non funziona, assicurati che il Bluetooth sia attivo",
                "Prova a chiudere e riaprire l'app",
                "Controlla che il codice sia stato inserito correttamente",
                "In caso di problemi, contattami subito"
            ],
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "device": "tv",
            "title": "Smart TV Samsung",
            "instructions": """La TV ha Netflix, YouTube e altre app preinstallate.
- Accendi con il telecomando (tasto rosso)
- Per Netflix: premi il tasto Netflix sul telecomando
- WiFi già connesso automaticamente
- Volume: tasti laterali del telecomando""",
            "troubleshooting": [
                "Se lo schermo è nero, controlla che la TV sia sulla sorgente corretta (HDMI1)",
                "Per problemi con Netflix, prova a riavviare la TV"
            ],
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "device": "climatizzatore",
            "title": "Aria Condizionata/Riscaldamento",
            "instructions": """Controllo climatizzatore:
- Telecomando sul muro vicino all'ingresso
- Tasto ON/OFF per accendere/spegnere
- MODE per cambiare tra freddo/caldo/deumidificatore
- Temperatura consigliata: 22-24°C
- Timer: tasto TIMER per programmazione""",
            "troubleshooting": [
                "Se non parte, attendere 3 minuti dopo l'accensione",
                "Chiudere le finestre per efficienza ottimale"
            ],
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "device": "lavatrice",
            "title": "Lavatrice Bosch",
            "instructions": """Uso lavatrice:
1. Carica i vestiti (max 7kg)
2. Aggiungi detersivo nel cassetto (già fornito)
3. Chiudi lo sportello
4. Seleziona programma con la manopola
5. Premi Start

Programmi consigliati:
- Cotone 40° per vestiti normali
- Delicati 30° per capi delicati
- Rapido 30min per rinfrescare""",
            "troubleshooting": [
                "Se non parte, controlla che lo sportello sia ben chiuso",
                "Il cassetto detersivo è in alto a sinistra"
            ],
            "created_at": datetime.now()
        },
        {
            "context_code": "apt_brescia",
            "device": "cucina",
            "title": "Piano Cottura a Induzione",
            "instructions": """Piano cottura a induzione:
- Usa SOLO pentole con fondo magnetico (quelle fornite)
- Touch control: tocca + o - per regolare potenza
- Timer: tasto orologio per impostare tempo cottura
- Blocco bambini: tieni premuto lucchetto 3 sec""",
            "troubleshooting": [
                "Se non si accende, controlla l'interruttore generale cucina",
                "Errore E: pentola non adatta, usa quelle fornite"
            ],
            "created_at": datetime.now()
        }
    ]
    
    smart_home_collection.insert_many(instructions)
    print(f"✅ Inserite {len(instructions)} istruzioni smart home")

def main():
    print("🏠 Inizializzazione dati Appartamento Brescia...")
    
    try:
        init_apartment_info()
        init_local_services()
        init_smart_home_instructions()
        
        print("\n✨ Dati appartamento inizializzati con successo!")
        print("\n📱 QR Code da creare:")
        print("   Festival: https://wa.me/34644409180?text=FESTIVAL_START")
        print("   Appartamento: https://wa.me/34644409180?text=APT_BRESCIA_START")
        
    except Exception as e:
        print(f"\n❌ Errore durante l'inizializzazione: {e}")

if __name__ == "__main__":
    main() 