#!/usr/bin/env python3
"""
Script per popolare il database con dati di esempio per l'appartamento di Brescia
"""

import os
from pymongo import MongoClient
from datetime import datetime

# Connessione MongoDB (usando variabili d'ambiente Render)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://Sergio:Ze76YKSpAuCjY.N@connyup.gqxa0sy.mongodb.net/?retryWrites=true&w=majority&appName=connyup")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "festival_db")

print(f"🔗 Connessione a MongoDB...")
print(f"   URI: {MONGODB_URI[:50]}...")
print(f"   Database: {MONGODB_DB_NAME}")

mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[MONGODB_DB_NAME]

# Collections
apartment_info_collection = db["apartment_info"]
local_services_collection = db["local_services"]
smart_home_collection = db["smart_home_instructions"]

def clean_existing_data():
    """Pulisce i dati esistenti per ricominciare"""
    print("🧹 Pulizia dati esistenti...")
    apartment_info_collection.delete_many({"context_code": "apt_brescia"})
    local_services_collection.delete_many({"context_code": "apt_brescia"})
    smart_home_collection.delete_many({"context_code": "apt_brescia"})
    print("✅ Dati esistenti rimossi")

def populate_apartment_info():
    """Popola le informazioni dell'appartamento"""
    print("🏠 Popolamento informazioni appartamento...")
    
    apartment_infos = [
        {
            "category": "check_in",
            "content": "Il check-in è dalle 15:00 alle 20:00. Le chiavi sono in una cassaforte digitale all'ingresso (codice: 1234). Per check-in tardivi, contattare il numero +39 030 123456.",
            "priority": 10,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "check_out",
            "content": "Il check-out è entro le 11:00. Lasciare le chiavi nella cassaforte e chiudere la porta. Portare via la spazzatura e lasciare l'appartamento pulito.",
            "priority": 9,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "wifi",
            "content": "Nome rete: SmeraldoWiFi | Password: Brescia2024! | La password è anche scritta sul frigorifero. Velocità: 100 Mbps.",
            "priority": 8,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "regole_casa",
            "content": "Non fumare in casa. Rispettare il silenzio dalle 22:00 alle 8:00. Massimo 4 ospiti. Separare la raccolta differenziata. Non lasciare finestre aperte quando si esce.",
            "priority": 7,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "parcheggio",
            "content": "Parcheggio gratuito in strada dopo le 19:00 e nei weekend. Parcheggio a pagamento Piazza della Loggia (5 min a piedi) - €1.50/ora.",
            "priority": 6,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "emergenze",
            "content": "Emergenze: 112 | Proprietario: +39 030 123456 | Ospedale Spedali Civili: +39 030 39951 | Farmacia notturna: Farmacia Centrale, Via Trieste 15",
            "priority": 10,
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    apartment_info_collection.insert_many(apartment_infos)
    print(f"✅ Aggiunte {len(apartment_infos)} informazioni appartamento")

def populate_local_services():
    """Popola i servizi locali"""
    print("📍 Popolamento servizi locali...")
    
    local_services = [
        # Ristoranti
        {
            "type": "restaurant",
            "name": "Osteria del Borgo",
            "description": "Cucina tradizionale bresciana con ingredienti locali. Ottimi casoncelli e polenta.",
            "address": "Via San Martino della Battaglia, 20",
            "distance": "3 minuti a piedi",
            "phone": "+39 030 234567",
            "rating": 4.5,
            "hours": "12:00-14:30, 19:00-23:00",
            "maps_url": "https://maps.google.com/?q=Osteria+del+Borgo+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "type": "restaurant",
            "name": "Pizzeria Da Marco",
            "description": "Pizza napoletana autentica con forno a legna. Ambiente familiare e prezzi onesti.",
            "address": "Via Giuseppe Mazzini, 45",
            "distance": "5 minuti a piedi",
            "phone": "+39 030 345678",
            "rating": 4.2,
            "hours": "18:30-24:00",
            "maps_url": "https://maps.google.com/?q=Pizzeria+Da+Marco+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Supermercati
        {
            "type": "supermarket",
            "name": "Conad City",
            "description": "Supermercato di vicinato con prodotti freschi, pane e articoli per la casa.",
            "address": "Via Trieste, 30",
            "distance": "2 minuti a piedi",
            "phone": "+39 030 456789",
            "rating": 4.0,
            "hours": "8:00-20:00",
            "maps_url": "https://maps.google.com/?q=Conad+City+Brescia+Trieste",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "type": "supermarket",
            "name": "Esselunga",
            "description": "Grande supermercato con ampia scelta e prodotti biologici. Parcheggio gratuito.",
            "address": "Via Milano, 100",
            "distance": "10 minuti in auto",
            "phone": "+39 030 567890",
            "rating": 4.3,
            "hours": "8:30-21:00",
            "maps_url": "https://maps.google.com/?q=Esselunga+Brescia+Milano",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Farmacie
        {
            "type": "pharmacy",
            "name": "Farmacia Centrale",
            "description": "Farmacia storica con servizio notturno e misurazione pressione gratuita.",
            "address": "Via Trieste, 15",
            "distance": "1 minuto a piedi",
            "phone": "+39 030 678901",
            "rating": 4.4,
            "hours": "8:30-19:30 (notturno ven-sab)",
            "maps_url": "https://maps.google.com/?q=Farmacia+Centrale+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Attrazioni
        {
            "type": "attraction",
            "name": "Castello di Brescia",
            "description": "Fortezza medievale con vista panoramica sulla città. Museo delle Armi e percorsi storici.",
            "address": "Via del Castello, 9",
            "distance": "15 minuti a piedi",
            "phone": "+39 030 789012",
            "rating": 4.6,
            "hours": "10:00-18:00 (mar-dom)",
            "maps_url": "https://maps.google.com/?q=Castello+di+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "type": "attraction",
            "name": "Piazza della Loggia",
            "description": "Cuore rinascimentale di Brescia con il famoso orologio astronomico e portici eleganti.",
            "address": "Piazza della Loggia",
            "distance": "5 minuti a piedi",
            "phone": "",
            "rating": 4.7,
            "hours": "Sempre aperto",
            "maps_url": "https://maps.google.com/?q=Piazza+della+Loggia+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Bar/Caffè
        {
            "type": "cafe",
            "name": "Caffè del Centro",
            "description": "Bar storico con ottimo caffè e cornetti freschi. Terrazza con vista sulla piazza.",
            "address": "Via Musei, 12",
            "distance": "4 minuti a piedi",
            "phone": "+39 030 890123",
            "rating": 4.3,
            "hours": "6:30-20:00",
            "maps_url": "https://maps.google.com/?q=Caffè+del+Centro+Brescia",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    local_services_collection.insert_many(local_services)
    print(f"✅ Aggiunti {len(local_services)} servizi locali")

def populate_smart_devices():
    """Popola i dispositivi smart home"""
    print("🏠 Popolamento dispositivi smart home...")
    
    smart_devices = [
        {
            "device": "Serratura Principale",
            "device_type": "lock",
            "instructions": "Serratura TTLock: Codice master: 123456. Per cambiare il codice, tenere premuto il tasto * per 3 secondi, inserire il codice master, poi il nuovo codice seguito da #. La batteria dura circa 6 mesi.",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "device": "Smart TV Samsung",
            "device_type": "tv",
            "instructions": "TV Samsung 55' con Netflix, Prime Video, Disney+. Telecomando vocale. Per YouTube, dire 'Ciao Bixby, apri YouTube'. WiFi già configurato. Account Netflix: ospite@smeraldo.com / password: Brescia2024",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "device": "Aria Condizionata",
            "device_type": "ac",
            "instructions": "Climatizzatore Daikin: Telecomando sul comodino. Modalità ECO consigliata (tasto verde). Timer autospegnimento dopo 8 ore. Non scendere sotto 22°C per risparmio energetico.",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "device": "Lavastoviglie",
            "device_type": "appliance",
            "instructions": "Lavastoviglie Bosch: Tabs già forniti nel cassetto. Programma ECO (2h 30min) per uso normale. Programma RAPIDO (30min) per pochi piatti. Aprire sempre dopo il lavaggio per asciugatura.",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "device": "Lavatrice",
            "device_type": "appliance",
            "instructions": "Lavatrice Samsung 8kg: Detersivo fornito nell'armadio bagno. Programma Cotone 40° per uso normale. Programma Delicati per lana/seta. Centrifuga massimo 1000 giri per capi delicati.",
            "context_code": "apt_brescia",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    smart_home_collection.insert_many(smart_devices)
    print(f"✅ Aggiunti {len(smart_devices)} dispositivi smart home")

def main():
    """Funzione principale"""
    print("🚀 Avvio popolamento database appartamento Brescia...")
    
    # Pulisce i dati esistenti
    clean_existing_data()
    
    # Popola con nuovi dati
    populate_apartment_info()
    populate_local_services()
    populate_smart_devices()
    
    print("\n🎉 Popolamento completato con successo!")
    print("📊 Riepilogo:")
    print(f"   • {apartment_info_collection.count_documents({'context_code': 'apt_brescia'})} informazioni appartamento")
    print(f"   • {local_services_collection.count_documents({'context_code': 'apt_brescia'})} servizi locali")
    print(f"   • {smart_home_collection.count_documents({'context_code': 'apt_brescia'})} dispositivi smart home")
    print("\n✅ Ora puoi testare l'admin panel all'URL: /admin/apartment")

if __name__ == "__main__":
    main() 