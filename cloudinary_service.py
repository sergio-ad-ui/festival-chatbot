#!/usr/bin/env python3
"""
Servizio per gestire upload e operazioni Cloudinary
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Dict, Optional

class CloudinaryService:
    """Servizio per gestire immagini con Cloudinary"""
    
    def __init__(self):
        """Inizializza Cloudinary con le credenziali"""
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dgo1dt0yb"),
            api_key=os.getenv("CLOUDINARY_API_KEY", "584381284578418"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET", "WdDav6Dhf6ER5KvaJ551ViSldtc")
        )
        
    def upload_image(self, file, folder: str = "connyup", context: str = "general") -> Optional[Dict]:
        """
        Upload di un'immagine su Cloudinary
        
        Args:
            file: File immagine da uploadare
            folder: Cartella di destinazione su Cloudinary
            context: Contesto (festival, apartment, etc.)
            
        Returns:
            Dict con URL e dettagli dell'immagine o None se errore
        """
        try:
            # Configurazione upload
            upload_options = {
                "folder": f"{folder}/{context}",
                "resource_type": "image",
                "format": "jpg",  # Converti tutto in JPG per consistenza
                "quality": "auto:good",  # Ottimizzazione automatica qualità
                "fetch_format": "auto",  # Formato ottimale per browser
                "flags": "progressive",  # Caricamento progressivo
                "transformation": [
                    {"width": 1200, "height": 800, "crop": "limit"},  # Max size
                    {"quality": "auto:good"}
                ]
            }
            
            # Upload
            result = cloudinary.uploader.upload(file, **upload_options)
            
            print(f"✅ Immagine caricata su Cloudinary: {result.get('public_id')}")
            
            return {
                "public_id": result.get("public_id"),
                "url": result.get("secure_url"),
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "bytes": result.get("bytes"),
                "created_at": result.get("created_at")
            }
            
        except Exception as e:
            print(f"❌ Errore upload Cloudinary: {e}")
            return None
    
    def get_optimized_url(self, public_id: str, width: int = 800, height: int = 600) -> str:
        """
        Genera URL ottimizzato per WhatsApp
        
        Args:
            public_id: ID pubblico dell'immagine su Cloudinary
            width: Larghezza desiderata
            height: Altezza desiderata
            
        Returns:
            URL ottimizzato
        """
        try:
            url, options = cloudinary.utils.cloudinary_url(
                public_id,
                width=width,
                height=height,
                crop="fill",
                gravity="center",
                quality="auto:good",
                fetch_format="auto"
            )
            return url
        except Exception as e:
            print(f"❌ Errore generazione URL ottimizzato: {e}")
            return ""
    
    def delete_image(self, public_id: str) -> bool:
        """
        Elimina un'immagine da Cloudinary
        
        Args:
            public_id: ID pubblico dell'immagine
            
        Returns:
            True se eliminata con successo
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
        except Exception as e:
            print(f"❌ Errore eliminazione immagine: {e}")
            return False
    
    def list_images(self, folder: str = "connyup") -> list:
        """
        Lista immagini in una cartella
        
        Args:
            folder: Nome cartella
            
        Returns:
            Lista di immagini
        """
        try:
            result = cloudinary.api.resources(
                type="upload",
                prefix=folder,
                max_results=100
            )
            return result.get("resources", [])
        except Exception as e:
            print(f"❌ Errore listing immagini: {e}")
            return []

# Istanza globale del servizio
cloudinary_service = CloudinaryService() 