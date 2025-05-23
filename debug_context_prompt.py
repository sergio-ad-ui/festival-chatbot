#!/usr/bin/env python3
"""
Script per debuggare il prompt del context manager
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from context_manager import ContextManager

# Carica le variabili d'ambiente
load_dotenv()

def test_context_prompt():
    print("🔍 DEBUG CONTEXT MANAGER PROMPT")
    print("=" * 50)
    
    # Configurazione MongoDB
    mongo_client = MongoClient(os.getenv("MONGODB_URI"))
    db = mongo_client[os.getenv("MONGODB_DB_NAME")]
    
    # Crea il context manager
    context_manager = ContextManager(db)
    
    print("1️⃣ Test identifica contesto:")
    context = context_manager.identify_context_from_message("Sono usciti gli orari?", "test_user")
    print(f"   Contesto identificato: {context}")
    
    print("\n2️⃣ Test get_context_info:")
    context_info = context_manager.get_context_info("festival")
    print(f"   Info contesto: {context_info}")
    
    print("\n3️⃣ Test get_context_prompt:")
    prompt = context_manager.get_context_prompt("festival")
    print(f"   Lunghezza prompt: {len(prompt)} caratteri")
    print(f"   Prompt generato:")
    print("-" * 40)
    print(prompt)
    print("-" * 40)
    
    print("\n4️⃣ Test dati festival nel database:")
    festival_collection = db["festival_info"]
    festival_data = list(festival_collection.find())
    print(f"   Numero voci festival in DB: {len(festival_data)}")
    
    if festival_data:
        print("   Dati trovati:")
        for i, item in enumerate(festival_data, 1):
            print(f"   {i}. {item.get('category', 'N/A')}: {item.get('content', 'N/A')[:50]}...")
    
    print("\n5️⃣ Analisi del problema:")
    if not festival_data:
        print("   ❌ PROBLEMA: Nessun dato festival nel database!")
    elif "dal 15 al 18 giugno 2025" not in prompt:
        print("   ❌ PROBLEMA: I dati del database non sono nel prompt!")
    elif len(prompt) < 200:
        print("   ❌ PROBLEMA: Prompt troppo corto, potrebbe non contenere i dati!")
    else:
        print("   ✅ TUTTO OK: Il prompt contiene i dati del festival!")
    
    return prompt

if __name__ == "__main__":
    test_context_prompt() 