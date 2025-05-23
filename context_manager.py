"""
Context Manager per il sistema multi-contesto del bot WhatsApp
Gestisce il routing e il caricamento delle informazioni specifiche per ogni contesto
"""

import re
from typing import Optional, Dict, List
from datetime import datetime
from pymongo import MongoClient
from pymongo.database import Database


class ContextManager:
    """Gestisce i diversi contesti del bot (festival, appartamenti, ecc.)"""
    
    # Mapping dei codici di avvio ai contesti
    START_CODES = {
        "FESTIVAL_START": "festival",
        "APT_BRESCIA_START": "apt_brescia",
        "APT_MILANO_START": "apt_milano",
        # Aggiungi altri codici qui
    }
    
    def __init__(self, db: Database):
        self.db = db
        self.contexts_collection = db["contexts"]
        self.apartment_info_collection = db["apartment_info"]
        self.local_services_collection = db["local_services"]
        self.smart_home_collection = db["smart_home_instructions"]
        self.festival_info_collection = db["festival_info"]
        
    def identify_context_from_message(self, message: str, sender_id: str) -> Optional[str]:
        """
        Identifica il contesto dal messaggio iniziale o dalla conversazione esistente
        """
        # Controlla se il messaggio contiene un codice di avvio
        message_upper = message.upper().strip()
        for code, context in self.START_CODES.items():
            if code in message_upper:
                return context
        
        # Se non c'è un codice, cerca una conversazione esistente
        conversation = self.db["conversations"].find_one({
            "sender_id": sender_id
        }, sort=[("last_updated", -1)])
        
        if conversation and "context" in conversation:
            return conversation["context"]
        
        # Default al festival se non si trova nulla
        return None
    
    def get_context_info(self, context_code: str) -> Optional[Dict]:
        """Recupera le informazioni di configurazione per un contesto"""
        return self.contexts_collection.find_one({"code": context_code, "active": True})
    
    def get_context_prompt(self, context_code: str) -> str:
        """Genera il prompt di sistema per il contesto specificato"""
        context_info = self.get_context_info(context_code)
        
        if not context_info:
            # Fallback per contesti non configurati
            if context_code == "festival":
                return self._get_festival_prompt()
            return "Sei un assistente virtuale. Rispondi in modo cordiale e professionale."
        
        # Costruisci il prompt base dal contesto
        prompt = context_info["system_prompt"]
        
        # Aggiungi informazioni specifiche in base al tipo di contesto
        if context_info["type"] == "apartment":
            prompt += self._get_apartment_context_additions(context_code)
        elif context_info["type"] == "festival":
            prompt += self._get_festival_context_additions()
            
        return prompt
    
    def _get_festival_prompt(self) -> str:
        """Genera il prompt per il contesto festival (compatibilità con il sistema esistente)"""
        festival_info = list(self.festival_info_collection.find())
        
        context = "Sei un assistente virtuale per il ConnyUp Festival. "
        context += "Il tuo compito è fornire informazioni accurate sull'evento, aiutare con le direzioni, "
        context += "spiegare gli orari e rispondere a domande sui servizi disponibili. "
        context += "Rispondi sempre in italiano in modo amichevole e entusiasta. "
        context += "Ecco le informazioni sul festival:\n\n"
        
        for info in festival_info:
            if "category" in info and "content" in info:
                context += f"{info['category']}: {info['content']}\n"
        
        return context
    
    def _get_apartment_context_additions(self, context_code: str) -> str:
        """Aggiunge informazioni specifiche per un appartamento al prompt"""
        additions = "\n\nInformazioni sull'appartamento:\n"
        
        # Carica info appartamento (senza filtro context_code per ora)
        # TODO: In futuro possiamo aggiungere filtri per appartamento specifico
        apartment_info = list(self.apartment_info_collection.find().sort("priority", 1))
        
        if apartment_info:
            for info in apartment_info:
                if info.get('category') and info.get('content'):
                    additions += f"\n{info['category']}: {info['content']}"
        
        # Carica servizi locali
        services = list(self.local_services_collection.find())
        
        if services:
            additions += "\n\nServizi nelle vicinanze:"
            
            # Raggruppa per tipo
            services_by_type = {}
            for service in services:
                service_type = service.get('type', 'other')
                if service_type not in services_by_type:
                    services_by_type[service_type] = []
                services_by_type[service_type].append(service)
            
            # Ordine preferito per i tipi
            type_order = ['restaurant', 'cafe', 'supermarket', 'pharmacy', 'attraction', 'transport', 'other']
            type_names = {
                'restaurant': 'Ristoranti',
                'cafe': 'Bar e Caffè', 
                'supermarket': 'Supermercati',
                'pharmacy': 'Farmacie',
                'attraction': 'Attrazioni',
                'transport': 'Trasporti',
                'other': 'Altri Servizi'
            }
            
            for service_type in type_order:
                if service_type in services_by_type:
                    additions += f"\n\n{type_names.get(service_type, service_type.title())}:"
                    for service in services_by_type[service_type]:
                        name = service.get('name', 'N/A')
                        description = service.get('description', '')
                        distance = service.get('distance', '')
                        rating = service.get('rating', '')
                        phone = service.get('phone', '')
                        hours = service.get('hours', '')
                        
                        additions += f"\n• {name}"
                        if description:
                            additions += f" - {description}"
                        if distance:
                            additions += f" ({distance})"
                        if rating:
                            additions += f" ⭐ {rating}/5"
                        if phone:
                            additions += f" Tel: {phone}"
                        if hours:
                            additions += f" Orari: {hours}"
        
        # Carica istruzioni smart home
        smart_instructions = list(self.smart_home_collection.find())
        
        if smart_instructions:
            additions += "\n\nDispositivi smart e istruzioni:"
            for instruction in smart_instructions:
                device = instruction.get('device', 'Dispositivo')
                instructions = instruction.get('instructions', '')
                device_type = instruction.get('device_type', '')
                
                additions += f"\n• {device}"
                if device_type:
                    additions += f" ({device_type})"
                if instructions:
                    additions += f": {instructions}"
        
        # Se non ci sono dati, restituisci un prompt base
        if not apartment_info and not services and not smart_instructions:
            additions = "\n\nNOTA: I dati specifici dell'appartamento non sono ancora stati configurati nell'admin panel."
        
        return additions
    
    def _get_festival_context_additions(self) -> str:
        """Aggiunge informazioni specifiche per il festival al prompt"""
        # Già gestito in _get_festival_prompt per compatibilità
        return ""
    
    def get_welcome_message(self, context_code: str) -> str:
        """Ottiene il messaggio di benvenuto per un contesto"""
        context_info = self.get_context_info(context_code)
        
        if context_info:
            return context_info["welcome_message"]
        
        # Fallback messages
        if context_code == "festival":
            return "🎪 Benvenuto al ConnyUp Festival! Come posso aiutarti?"
        elif "apt_" in context_code:
            return "🏠 Benvenuto! Sono qui per aiutarti durante il tuo soggiorno. Come posso esserti utile?"
        
        return "👋 Ciao! Come posso aiutarti?"
    
    def should_show_context_menu(self, message: str) -> bool:
        """Determina se mostrare il menu di selezione contesto"""
        # Mostra il menu se l'utente scrive "menu", "start", "inizio", ecc.
        trigger_words = ["menu", "start", "inizio", "aiuto", "help", "ciao", "salve"]
        message_lower = message.lower().strip()
        
        return any(word in message_lower for word in trigger_words) and len(message_lower) < 20
    
    def get_context_menu(self) -> str:
        """Genera il menu di selezione contesto"""
        active_contexts = list(self.contexts_collection.find({"active": True}))
        
        if not active_contexts:
            # Fallback se non ci sono contesti configurati
            return """👋 Ciao! Sono un assistente virtuale. Posso aiutarti con:
            
1️⃣ Festival ConnyUp - Scrivi FESTIVAL_START
2️⃣ Appartamento Brescia - Scrivi APT_BRESCIA_START

Cosa ti interessa?"""
        
        menu = "👋 Ciao! Sono un assistente virtuale. Posso aiutarti con:\n\n"
        
        for i, context in enumerate(active_contexts, 1):
            # Trova il codice di avvio per questo contesto
            start_code = next(
                (code for code, ctx in self.START_CODES.items() if ctx == context["code"]),
                f"{context['code'].upper()}_START"
            )
            menu += f"{i}️⃣ {context['name']} - Scrivi {start_code}\n"
        
        menu += "\nCosa ti interessa?"
        return menu
    
    def initialize_default_contexts(self):
        """Inizializza i contesti di default se non esistono"""
        # Controlla se esistono già contesti
        if self.contexts_collection.count_documents({}) > 0:
            return
        
        # Crea contesto Festival
        festival_context = {
            "code": "festival",
            "name": "ConnyUp Festival",
            "type": "festival",
            "welcome_message": "🎪 Benvenuto al ConnyUp Festival! Sono qui per fornirti tutte le informazioni sull'evento. Come posso aiutarti?",
            "system_prompt": "Sei un assistente virtuale entusiasta e competente per il ConnyUp Festival. Fornisci informazioni accurate su orari, location, artisti e servizi. Rispondi sempre in italiano in modo amichevole.",
            "active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Crea contesto Appartamento Brescia
        apt_brescia_context = {
            "code": "apt_brescia",
            "name": "Appartamento Smeraldo Brescia",
            "type": "apartment",
            "welcome_message": "🏠 Benvenuto all'Appartamento Smeraldo! Sono il tuo assistente virtuale e sono qui per rendere il tuo soggiorno perfetto. Posso aiutarti con check-in, WiFi, consigli sui ristoranti e molto altro!",
            "system_prompt": "Sei un assistente virtuale per gli ospiti dell'Appartamento Smeraldo a Brescia. Sei cordiale, professionale e molto disponibile. Fornisci informazioni dettagliate su: check-in/out, WiFi, dispositivi smart home (TTLock), regole della casa, servizi locali e attrazioni. Rispondi sempre in italiano.",
            "active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        self.contexts_collection.insert_many([festival_context, apt_brescia_context]) 