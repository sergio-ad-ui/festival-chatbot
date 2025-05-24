from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from bson import ObjectId
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Importo il servizio Cloudinary
from cloudinary_service import cloudinary_service

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DB_NAME")]

# Collections per Festival (legacy)
festival_info_collection = db["festival_info"]
events_collection = db["events"]
map_points_collection = db["map_points"]

# Collections per Multi-Contesto (nuovo)
contexts_collection = db["contexts"]
apartment_info_collection = db["apartment_info"]
local_services_collection = db["local_services"]
smart_home_collection = db["smart_home_instructions"]
conversations_collection = db["conversations"]

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ================================
# ROUTE PRINCIPALI MULTI-CONTESTO
# ================================

@admin_bp.route('/')
def index():
    """Dashboard principale multi-contesto"""
    return render_template('admin/main.html')

@admin_bp.route('/festival')
def festival_admin():
    """Admin specifico per il contesto Festival (legacy)"""
    return render_template('admin/index.html')

@admin_bp.route('/apartment')
def apartment_admin():
    """Admin specifico per il contesto Appartamenti"""
    return render_template('admin/apartment.html')

@admin_bp.route('/images')
def images_admin():
    """Admin per gestione immagini Cloudinary"""
    return render_template('admin/images.html')

# ================================
# API STATISTICHE GLOBALI
# ================================

@admin_bp.route('/api/stats')
def global_stats():
    """API per statistiche globali dashboard"""
    try:
        # Conteggio conversazioni per contesto
        total_conversations = conversations_collection.count_documents({})
        festival_conversations = conversations_collection.count_documents({"context": "festival"})
        apartment_conversations = conversations_collection.count_documents({"context": "apartment"})
        
        # Utenti unici
        unique_users = len(conversations_collection.distinct("sender_id"))
        
        # Conteggio dati per contesto
        festival_info_count = festival_info_collection.count_documents({})
        apartment_count = apartment_info_collection.count_documents({})
        checkins_count = apartment_conversations  # Proxy per check-ins
        
        # Tempo medio risposta (simulato)
        avg_response_time = 850  # ms simulato
        satisfaction_rate = 94   # % simulato
        
        stats = {
            "total_conversations": total_conversations,
            "total_users": unique_users,
            "avg_response_time": avg_response_time,
            "satisfaction_rate": satisfaction_rate,
            "festival_info_count": festival_info_count,
            "festival_conversations": festival_conversations,
            "apartment_count": apartment_count,
            "checkins_count": checkins_count
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# API APPARTAMENTI
# ================================

@admin_bp.route('/api/apartment-info', methods=['GET', 'POST'])
def apartment_info_api():
    """API per gestire informazioni appartamenti"""
    if request.method == 'POST':
        data = request.json
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        
        # Aggiungi context_code automaticamente se non presente
        if 'context_code' not in data:
            data['context_code'] = 'apt_brescia'  # Default per ora
        
        if '_id' in data:
            # Aggiornamento
            info_id = data.pop('_id')
            data['updated_at'] = datetime.now()
            apartment_info_collection.update_one(
                {'_id': ObjectId(info_id)},
                {'$set': data}
            )
            # Reset conversazioni appartamenti quando dati aggiornati
            reset_count = reset_active_conversations(db, "apt_brescia")
            return jsonify({'success': True, 'message': f'Informazione aggiornata. Reset {reset_count} conversazioni.'})
        else:
            # Nuova informazione
            result = apartment_info_collection.insert_one(data)
            # Reset conversazioni appartamenti per nuovi dati
            reset_count = reset_active_conversations(db, "apt_brescia")
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': f'Informazione aggiunta. Reset {reset_count} conversazioni.'})
    
    # GET - Restituisci tutte le informazioni
    apartment_info = list(apartment_info_collection.find())
    for info in apartment_info:
        info['_id'] = str(info['_id'])
    
    return jsonify(apartment_info)

@admin_bp.route('/api/apartment-info/<info_id>', methods=['DELETE'])
def delete_apartment_info(info_id):
    """Elimina informazione appartamento"""
    apartment_info_collection.delete_one({'_id': ObjectId(info_id)})
    return jsonify({'success': True, 'message': 'Informazione eliminata'})

@admin_bp.route('/api/local-services', methods=['GET', 'POST'])
def local_services_api():
    """API per gestire servizi locali"""
    if request.method == 'POST':
        data = request.json
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        
        # Aggiungi context_code automaticamente se non presente
        if 'context_code' not in data:
            data['context_code'] = 'apt_brescia'  # Default per ora
        
        if '_id' in data:
            service_id = data.pop('_id')
            data['updated_at'] = datetime.now()
            local_services_collection.update_one(
                {'_id': ObjectId(service_id)},
                {'$set': data}
            )
            return jsonify({'success': True, 'message': 'Servizio aggiornato'})
        else:
            result = local_services_collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': 'Servizio aggiunto'})
    
    # GET - con filtri opzionali
    service_type = request.args.get('type')
    query = {}
    if service_type and service_type != 'all':
        query['type'] = service_type
    
    services = list(local_services_collection.find(query))
    for service in services:
        service['_id'] = str(service['_id'])
    
    return jsonify(services)

@admin_bp.route('/api/local-services/<service_id>', methods=['DELETE'])
def delete_local_service(service_id):
    """Elimina servizio locale"""
    local_services_collection.delete_one({'_id': ObjectId(service_id)})
    return jsonify({'success': True, 'message': 'Servizio eliminato'})

@admin_bp.route('/api/smart-home', methods=['GET', 'POST'])
def smart_home_api():
    """API per dispositivi smart home"""
    if request.method == 'POST':
        data = request.json
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        
        # Aggiungi context_code automaticamente se non presente
        if 'context_code' not in data:
            data['context_code'] = 'apt_brescia'  # Default per ora
        
        if '_id' in data:
            device_id = data.pop('_id')
            data['updated_at'] = datetime.now()
            smart_home_collection.update_one(
                {'_id': ObjectId(device_id)},
                {'$set': data}
            )
            return jsonify({'success': True, 'message': 'Dispositivo aggiornato'})
        else:
            result = smart_home_collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': 'Dispositivo aggiunto'})
    
    devices = list(smart_home_collection.find())
    for device in devices:
        device['_id'] = str(device['_id'])
    
    return jsonify(devices)

@admin_bp.route('/api/smart-home/<device_id>', methods=['DELETE'])
def delete_smart_device(device_id):
    """Elimina dispositivo smart home"""
    smart_home_collection.delete_one({'_id': ObjectId(device_id)})
    return jsonify({'success': True, 'message': 'Dispositivo eliminato'})

@admin_bp.route('/api/conversations')
def conversations_api():
    """API per conversazioni recenti"""
    context = request.args.get('context', 'all')
    limit = int(request.args.get('limit', 50))
    
    query = {}
    if context != 'all':
        query['context'] = context
    
    conversations = list(conversations_collection.find(query)
                        .sort("last_updated", -1)
                        .limit(limit))
    
    for conv in conversations:
        conv['_id'] = str(conv['_id'])
        # Mostra solo gli ultimi 2 messaggi per privacy
        if 'messages' in conv and len(conv['messages']) > 2:
            conv['messages'] = conv['messages'][-2:]
    
    return jsonify(conversations)

# ================================
# API FESTIVAL (LEGACY SUPPORT)
# ================================

@admin_bp.route('/festival-info', methods=['GET', 'POST'])
def festival_info():
    """API Festival Info (legacy)"""
    if request.method == 'POST':
        data = request.json
        if '_id' in data:
            info_id = data.pop('_id')
            festival_info_collection.update_one(
                {'_id': ObjectId(info_id)},
                {'$set': data}
            )
            # Reset conversazioni festival quando dati aggiornati
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'message': f'Informazione aggiornata. Reset {reset_count} conversazioni.'})
        else:
            result = festival_info_collection.insert_one(data)
            # Reset conversazioni festival per nuovi dati
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': f'Informazione aggiunta. Reset {reset_count} conversazioni.'})
    
    festival_info = list(festival_info_collection.find())
    for info in festival_info:
        info['_id'] = str(info['_id'])
    
    return jsonify(festival_info)

@admin_bp.route('/festival-info/<info_id>', methods=['GET'])
def get_single_festival_info(info_id):
    """Ottiene una singola informazione festival"""
    info = festival_info_collection.find_one({'_id': ObjectId(info_id)})
    if info:
        info['_id'] = str(info['_id'])
        return jsonify(info)
    return jsonify({'error': 'Informazione non trovata'}), 404

@admin_bp.route('/festival-info/<info_id>', methods=['DELETE'])
def delete_festival_info(info_id):
    festival_info_collection.delete_one({'_id': ObjectId(info_id)})
    return jsonify({'success': True, 'message': 'Informazione eliminata'})

@admin_bp.route('/events', methods=['GET', 'POST'])
def events():
    """API Eventi Festival (legacy)"""
    if request.method == 'POST':
        data = request.json
        if '_id' in data:
            event_id = data.pop('_id')
            events_collection.update_one(
                {'_id': ObjectId(event_id)},
                {'$set': data}
            )
            # Reset conversazioni festival quando eventi aggiornati
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'message': f'Evento aggiornato. Reset {reset_count} conversazioni.'})
        else:
            result = events_collection.insert_one(data)
            # Reset conversazioni festival per nuovi eventi
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': f'Evento aggiunto. Reset {reset_count} conversazioni.'})
    
    events = list(events_collection.find())
    for event in events:
        event['_id'] = str(event['_id'])
    
    return jsonify(events)

@admin_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events_collection.delete_one({'_id': ObjectId(event_id)})
    # Reset conversazioni festival quando evento eliminato
    reset_count = reset_active_conversations(db, "festival")
    return jsonify({'success': True, 'message': f'Evento eliminato. Reset {reset_count} conversazioni.'})

@admin_bp.route('/map', methods=['GET', 'POST'])
def map():
    """API Mappa Festival (legacy)"""
    if request.method == 'POST':
        data = request.json
        if '_id' in data:
            point_id = data.pop('_id')
            map_points_collection.update_one(
                {'_id': ObjectId(point_id)},
                {'$set': data}
            )
            # Reset conversazioni festival quando mappa aggiornata
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'message': f'Punto mappa aggiornato. Reset {reset_count} conversazioni.'})
        else:
            result = map_points_collection.insert_one(data)
            # Reset conversazioni festival per nuovi punti mappa
            reset_count = reset_active_conversations(db, "festival")
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': f'Punto mappa aggiunto. Reset {reset_count} conversazioni.'})
    
    map_points = list(map_points_collection.find())
    for point in map_points:
        point['_id'] = str(point['_id'])
    
    return jsonify(map_points)

@admin_bp.route('/map/<point_id>', methods=['DELETE'])
def delete_map_point(point_id):
    map_points_collection.delete_one({'_id': ObjectId(point_id)})
    # Reset conversazioni festival quando punto mappa eliminato
    reset_count = reset_active_conversations(db, "festival")
    return jsonify({'success': True, 'message': f'Punto mappa eliminato. Reset {reset_count} conversazioni.'})

# ================================
# API CLOUDINARY - GESTIONE IMMAGINI
# ================================

@admin_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Upload di un'immagine su Cloudinary"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nessun file immagine fornito'}), 400
        
        file = request.files['image']
        context = request.form.get('context', 'general')  # festival, apartment, general
        title = request.form.get('title', '')
        
        if file.filename == '':
            return jsonify({'error': 'Nessun file selezionato'}), 400
        
        # Upload su Cloudinary
        result = cloudinary_service.upload_image(file, context=context)
        
        if result:
            # Salva informazioni nel database per gestione
            image_data = {
                'public_id': result['public_id'],
                'url': result['url'],
                'title': title,
                'context': context,
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format'),
                'bytes': result.get('bytes'),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Salva in collezione immagini
            images_collection = db["images"]
            db_result = images_collection.insert_one(image_data)
            image_data['_id'] = str(db_result.inserted_id)
            
            return jsonify({
                'success': True,
                'image': image_data,
                'message': 'Immagine caricata con successo'
            })
        else:
            return jsonify({'error': 'Errore durante l\'upload su Cloudinary'}), 500
            
    except Exception as e:
        print(f"❌ Errore upload immagine: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/images', methods=['GET'])
def list_images():
    """Lista immagini caricate"""
    try:
        context = request.args.get('context', 'all')
        
        query = {}
        if context != 'all':
            query['context'] = context
        
        images_collection = db["images"]
        images = list(images_collection.find(query).sort('created_at', -1))
        
        for image in images:
            image['_id'] = str(image['_id'])
            # Aggiungi URL ottimizzato per preview
            image['thumbnail_url'] = cloudinary_service.get_optimized_url(
                image['public_id'], width=300, height=200
            )
        
        return jsonify(images)
        
    except Exception as e:
        print(f"❌ Errore listing immagini: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    """Elimina un'immagine"""
    try:
        images_collection = db["images"]
        image = images_collection.find_one({'_id': ObjectId(image_id)})
        
        if not image:
            return jsonify({'error': 'Immagine non trovata'}), 404
        
        # Elimina da Cloudinary
        deleted = cloudinary_service.delete_image(image['public_id'])
        
        if deleted:
            # Elimina dal database
            images_collection.delete_one({'_id': ObjectId(image_id)})
            return jsonify({'success': True, 'message': 'Immagine eliminata'})
        else:
            return jsonify({'error': 'Errore durante l\'eliminazione da Cloudinary'}), 500
            
    except Exception as e:
        print(f"❌ Errore eliminazione immagine: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/images/<image_id>', methods=['PUT'])
def update_image(image_id):
    """Aggiorna metadati di un'immagine"""
    try:
        data = request.json
        images_collection = db["images"]
        
        update_data = {
            'title': data.get('title', ''),
            'context': data.get('context', 'general'),
            'updated_at': datetime.now()
        }
        
        result = images_collection.update_one(
            {'_id': ObjectId(image_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return jsonify({'success': True, 'message': 'Immagine aggiornata'})
        else:
            return jsonify({'error': 'Immagine non trovata'}), 404
            
    except Exception as e:
        print(f"❌ Errore aggiornamento immagine: {e}")
        return jsonify({'error': str(e)}), 500

def reset_active_conversations(db, context_type=None):
    """Reset soft delle conversazioni: mantiene contesto ma elimina messaggi"""
    try:
        query = {}
        if context_type:
            query["context"] = context_type
        
        # Reset SOFT: mantieni conversazione ma svuota messaggi e resetta timestamp
        update_data = {
            "$set": {
                "messages": [],
                "last_updated": datetime.now(),
                "reset_reason": "admin_data_update"
            }
        }
        
        result = db["conversations"].update_many(query, update_data)
        print(f"🔄 RESET SOFT: Aggiornate {result.modified_count} conversazioni (messaggi eliminati, contesto mantenuto)")
        return result.modified_count
    except Exception as e:
        print(f"❌ Errore nel reset conversazioni: {e}")
        return 0

# Registra il blueprint nell'app principale
def register_admin_routes(app):
    app.register_blueprint(admin_bp) 