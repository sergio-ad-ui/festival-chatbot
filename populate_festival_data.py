#!/usr/bin/env python3
"""
Script per popolare il database con dati di esempio per il ConnyUp Festival
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
festival_info_collection = db["festival_info"]
events_collection = db["events"]
map_points_collection = db["map_points"]

def clean_existing_data():
    """Pulisce i dati esistenti per ricominciare"""
    print("🧹 Pulizia dati esistenti...")
    festival_info_collection.delete_many({})
    events_collection.delete_many({})
    map_points_collection.delete_many({})
    print("✅ Dati esistenti rimossi")

def populate_festival_info():
    """Popola le informazioni generali del festival"""
    print("🎪 Popolamento informazioni festival...")
    
    festival_infos = [
        {
            "category": "date",
            "content": "dal 15 al 18 giugno 2025",
            "priority": 10,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "orari",
            "content": "DALLE 16.30 in poi tutti i giorni. Ultimo ingresso ore 01:00. Domenica chiusura anticipata alle 24:00.",
            "priority": 9,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "location",
            "content": "Parco Cascina San Giuseppe, Via dei Festival 25, Brescia. Facilmente raggiungibile con mezzi pubblici (linea bus 14) o auto (parcheggio gratuito disponibile).",
            "priority": 8,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "biglietti",
            "content": "Ingresso giornaliero: €25. Abbonamento 4 giorni: €80. Under 18: €15. Prevendita online su www.connyupfestival.it con sconto 20%. Biglietti disponibili anche in loco.",
            "priority": 7,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "parcheggio",
            "content": "Parcheggio gratuito disponibile nell'area festival (500 posti). Parcheggi aggiuntivi a pagamento in Piazza Brescia (€3/giorno) a 10 minuti a piedi.",
            "priority": 6,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "food_drink",
            "content": "15 stand gastronomici con cucina locale e internazionale. 4 bar con cocktail, birre artigianali e bevande analcoliche. Prezzi accessibili: panini €6-8, birra €4-6, cocktail €8-12.",
            "priority": 5,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "servizi",
            "content": "Guardaroba gratuito, servizi igienici, area fumatori, punto primo soccorso, bancomat, ricarica telefoni. WiFi gratuito nell'area festival (rete: ConnyUp-Free).",
            "priority": 4,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "regolamento",
            "content": "Vietato introdurre bevande alcoliche, oggetti di vetro, spray, droghe. Controlli all'ingresso. Consentite bottigliette di plastica vuote. Area fumatori dedicata.",
            "priority": 3,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "category": "contatti",
            "content": "Info: +39 030 555-0123 | Email: info@connyupfestival.it | Social: @connyupfestival | Emergenze: contattare staff con pettorina gialla",
            "priority": 10,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    festival_info_collection.insert_many(festival_infos)
    print(f"✅ Aggiunte {len(festival_infos)} informazioni festival")

def populate_events():
    """Popola gli eventi del festival"""
    print("🎵 Popolamento eventi e programma...")
    
    events = [
        # Giovedì 15 Giugno
        {
            "name": "Opening Night con DJ Marco Venturi",
            "description": "Serata di apertura con il celebre DJ internazionale Marco Venturi. Set di 3 ore con i migliori hits dance e house.",
            "start_time": "2025-06-15T19:00:00",
            "end_time": "2025-06-15T23:00:00",
            "location": "Main Stage",
            "artists": "DJ Marco Venturi, Local DJs Support",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Live Band: The Electric Souls",
            "description": "Band indie rock emergente con sonorità moderne e testi in italiano. Primo album appena uscito.",
            "start_time": "2025-06-15T21:30:00",
            "end_time": "2025-06-15T22:45:00",
            "location": "Acoustic Stage",
            "artists": "The Electric Souls",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Venerdì 16 Giugno
        {
            "name": "Concerto: Francesca Michielin",
            "description": "L'artista veneta presenta il suo nuovo tour con brani inediti e i suoi più grandi successi.",
            "start_time": "2025-06-16T21:00:00",
            "end_time": "2025-06-16T22:30:00",
            "location": "Main Stage",
            "artists": "Francesca Michielin",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "DJ Set: Techno Underground",
            "description": "Serata techno con i migliori DJ della scena underground italiana. Musica fino all'alba.",
            "start_time": "2025-06-16T23:00:00",
            "end_time": "2025-06-17T02:00:00",
            "location": "Electronic Area",
            "artists": "DJ Alex Neri, DJ Luca Agnelli, DJ Davide Squillace",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Workshop: Produzione Musicale",
            "description": "Masterclass gratuita sulla produzione musicale digitale con software professionali.",
            "start_time": "2025-06-16T17:00:00",
            "end_time": "2025-06-16T19:00:00",
            "location": "Workshop Area",
            "artists": "Producer Marco Bianchi",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Sabato 17 Giugno
        {
            "name": "Headliner: Subsonica",
            "description": "I leggendari Subsonica tornano live con il loro sound unico che ha fatto la storia della musica italiana.",
            "start_time": "2025-06-17T22:00:00",
            "end_time": "2025-06-17T23:45:00",
            "location": "Main Stage",
            "artists": "Subsonica",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Rapper: Nitro",
            "description": "Il rapper milanese presenta il suo ultimo album con uno show esplosivo e ospiti speciali.",
            "start_time": "2025-06-17T20:00:00",
            "end_time": "2025-06-17T21:15:00",
            "location": "Main Stage",
            "artists": "Nitro",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Showcase: Nuovi Talenti",
            "description": "Vetrina per giovani artisti emergenti selezionati tramite contest. 6 artisti, 15 minuti ciascuno.",
            "start_time": "2025-06-17T17:30:00",
            "end_time": "2025-06-17T19:00:00",
            "location": "Acoustic Stage",
            "artists": "Vari artisti emergenti",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Domenica 18 Giugno
        {
            "name": "Finale: Marlene Kuntz",
            "description": "Gran finale del festival con la storica band cuneese. Concerto acustico speciale e brani riarrangiati.",
            "start_time": "2025-06-18T21:00:00",
            "end_time": "2025-06-18T22:30:00",
            "location": "Main Stage",
            "artists": "Marlene Kuntz",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Jam Session Finale",
            "description": "Sessione aperta dove tutti gli artisti del festival si uniscono per improvvisazioni musicali.",
            "start_time": "2025-06-18T23:00:00",
            "end_time": "2025-06-18T24:00:00",
            "location": "All Stages",
            "artists": "Tutti gli artisti del festival",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    events_collection.insert_many(events)
    print(f"✅ Aggiunti {len(events)} eventi al programma")

def populate_map_points():
    """Popola i punti di interesse sulla mappa"""
    print("🗺️ Popolamento punti mappa...")
    
    map_points = [
        # Palchi
        {
            "name": "Main Stage",
            "type": "stage",
            "description": "Palco principale per i concerti degli headliner. Capienza 8000 persone con sound system professionale.",
            "lat": 45.5416,
            "lng": 10.2118,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Acoustic Stage",
            "type": "stage", 
            "description": "Palco acustico per concerti intimi e showcase. Atmosfera raccolta con sedute disponibili.",
            "lat": 45.5422,
            "lng": 10.2125,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Electronic Area",
            "type": "stage",
            "description": "Area dedicata alla musica elettronica con sistema audio specifico per bassi potenti.",
            "lat": 45.5410,
            "lng": 10.2130,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Area Food & Drink
        {
            "name": "Food Court Centrale",
            "type": "food",
            "description": "Area principale con 8 stand gastronomici: pizza, hamburger, cucina etnica, vegetariano, dolci.",
            "lat": 45.5419,
            "lng": 10.2122,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Bar Principale",
            "type": "food",
            "description": "Bar centrale con cocktail, birre alla spina, vini e analcolici. Terrazza panoramica al primo piano.",
            "lat": 45.5415,
            "lng": 10.2115,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Birreria Artigianale",
            "type": "food",
            "description": "Stand specializzato in birre artigianali locali e snacks gourmet. 12 birre alla spina.",
            "lat": 45.5425,
            "lng": 10.2128,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Servizi
        {
            "name": "Ingresso Principale",
            "type": "entrance",
            "description": "Entrata principale con controlli di sicurezza, info point e biglietteria. Aperto dalle 16:00.",
            "lat": 45.5408,
            "lng": 10.2110,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Ingresso Secondario",
            "type": "entrance", 
            "description": "Ingresso alternativo dal parcheggio. Controlli rapidi per abbonati.",
            "lat": 45.5428,
            "lng": 10.2135,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Info Point Centrale",
            "type": "info",
            "description": "Punto informazioni con staff multilingue, programma dettagliato, biglietti last minute, oggetti smarriti.",
            "lat": 45.5418,
            "lng": 10.2120,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Primo Soccorso",
            "type": "info",
            "description": "Punto di primo soccorso con personale medico qualificato. Attivo H24 durante il festival.",
            "lat": 45.5412,
            "lng": 10.2117,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Servizi Igienici Zona A",
            "type": "toilet",
            "description": "Servizi igienici principali con bagni accessibili e fasciatoio. Pulizia ogni ora.",
            "lat": 45.5420,
            "lng": 10.2113,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Servizi Igienici Zona B",
            "type": "toilet",
            "description": "Servizi secondari vicino all'Electronic Area. Include docce a gettoni.",
            "lat": 45.5413,
            "lng": 10.2132,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        
        # Altri punti di interesse
        {
            "name": "Workshop Area",
            "type": "other",
            "description": "Spazio coperto per workshop, masterclass e incontri. Capacità 100 persone sedute.",
            "lat": 45.5424,
            "lng": 10.2121,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Merchandising Ufficiale",
            "type": "other",
            "description": "Stand con gadgets ufficiali del festival: t-shirt, cappellini, borse, poster degli artisti.",
            "lat": 45.5417,
            "lng": 10.2126,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "name": "Area Relax",
            "type": "other",
            "description": "Zona verde con sedute, amache e ricarica telefoni. Perfetta per pause tra concerti.",
            "lat": 45.5421,
            "lng": 10.2116,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    map_points_collection.insert_many(map_points)
    print(f"✅ Aggiunti {len(map_points)} punti sulla mappa")

def main():
    """Funzione principale"""
    print("🚀 Avvio popolamento database ConnyUp Festival...")
    
    # Pulisce i dati esistenti
    clean_existing_data()
    
    # Popola con nuovi dati
    populate_festival_info()
    populate_events()
    populate_map_points()
    
    print("\n🎉 Popolamento completato con successo!")
    print("📊 Riepilogo:")
    print(f"   • {festival_info_collection.count_documents({})} informazioni festival")
    print(f"   • {events_collection.count_documents({})} eventi in programma")
    print(f"   • {map_points_collection.count_documents({})} punti sulla mappa")
    print("\n✅ Ora puoi testare l'admin panel all'URL: /admin/festival")

if __name__ == "__main__":
    main() 