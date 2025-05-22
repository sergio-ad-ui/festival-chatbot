from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from bson import ObjectId
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

# Configurazione MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DB_NAME")]
festival_info_collection = db["festival_info"]
events_collection = db["events"]
map_points_collection = db["map_points"]

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    return render_template('admin/index.html')

@admin_bp.route('/festival-info', methods=['GET', 'POST'])
def festival_info():
    if request.method == 'POST':
        # Gestisci la richiesta POST per aggiungere/aggiornare informazioni
        data = request.json
        if '_id' in data:
            # Aggiornamento
            info_id = data.pop('_id')
            festival_info_collection.update_one(
                {'_id': ObjectId(info_id)},
                {'$set': data}
            )
            return jsonify({'success': True, 'message': 'Informazione aggiornata'})
        else:
            # Nuova informazione
            result = festival_info_collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': 'Informazione aggiunta'})
    
    # Restituisci tutte le informazioni sul festival
    festival_info = list(festival_info_collection.find())
    for info in festival_info:
        info['_id'] = str(info['_id'])
    
    return jsonify(festival_info)

@admin_bp.route('/festival-info/<info_id>', methods=['DELETE'])
def delete_festival_info(info_id):
    festival_info_collection.delete_one({'_id': ObjectId(info_id)})
    return jsonify({'success': True, 'message': 'Informazione eliminata'})

@admin_bp.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        data = request.json
        if '_id' in data:
            event_id = data.pop('_id')
            events_collection.update_one(
                {'_id': ObjectId(event_id)},
                {'$set': data}
            )
            return jsonify({'success': True, 'message': 'Evento aggiornato'})
        else:
            result = events_collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': 'Evento aggiunto'})
    
    events = list(events_collection.find())
    for event in events:
        event['_id'] = str(event['_id'])
    
    return jsonify(events)

@admin_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events_collection.delete_one({'_id': ObjectId(event_id)})
    return jsonify({'success': True, 'message': 'Evento eliminato'})

@admin_bp.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        data = request.json
        if '_id' in data:
            point_id = data.pop('_id')
            map_points_collection.update_one(
                {'_id': ObjectId(point_id)},
                {'$set': data}
            )
            return jsonify({'success': True, 'message': 'Punto mappa aggiornato'})
        else:
            result = map_points_collection.insert_one(data)
            return jsonify({'success': True, 'id': str(result.inserted_id), 'message': 'Punto mappa aggiunto'})
    
    map_points = list(map_points_collection.find())
    for point in map_points:
        point['_id'] = str(point['_id'])
    
    return jsonify(map_points)

@admin_bp.route('/map/<point_id>', methods=['DELETE'])
def delete_map_point(point_id):
    map_points_collection.delete_one({'_id': ObjectId(point_id)})
    return jsonify({'success': True, 'message': 'Punto mappa eliminato'})

# Registra il blueprint nell'app principale
def register_admin_routes(app):
    app.register_blueprint(admin_bp) 