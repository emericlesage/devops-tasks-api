from flask import Blueprint, jsonify, request, current_app
from .models import init_db, get_all_users, create_user
from .config import get_redis_client
import psycopg2

bp = Blueprint('main', __name__)

@bp.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint"""
    health_status = {
        'status': 'healthy',
        'api': 'ok'
    }
    
    # Vérifier PostgreSQL
    try:
        conn = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD']
        )
        conn.close()
        health_status['database'] = 'ok'
    except Exception as e:
        health_status['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Vérifier Redis
    try:
        redis_client = get_redis_client()
        redis_client.ping()
        health_status['redis'] = 'ok'
    except Exception as e:
        health_status['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@bp.route('/init', methods=['POST'])
def initialize():
    """Initialiser la base de données"""
    try:
        init_db()
        return jsonify({'message': 'Database initialized successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users', methods=['GET'])
def get_users():
    """Récupérer tous les utilisateurs (avec cache Redis)"""
    redis_client = get_redis_client()
    
    # Vérifier le cache
    cached = redis_client.get('users:all')
    if cached:
        import json
        return jsonify({
            'users': json.loads(cached),
            'source': 'cache'
        }), 200
    
    # Sinon, récupérer de la DB
    users = get_all_users()
    
    # Mettre en cache pour 60 secondes
    import json
    redis_client.setex('users:all', 60, json.dumps(users))
    
    return jsonify({
        'users': users,
        'source': 'database'
    }), 200

@bp.route('/users', methods=['POST'])
def add_user():
    """Créer un nouvel utilisateur"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing name or email'}), 400
    
    user_id = create_user(data['name'], data['email'])
    
    if user_id is None:
        return jsonify({'error': 'Email already exists'}), 409
    
    # Invalider le cache
    redis_client = get_redis_client()
    redis_client.delete('users:all')
    
    return jsonify({
        'id': user_id,
        'name': data['name'],
        'email': data['email']
    }), 201

@bp.route('/', methods=['GET'])
def index():
    """Page d'accueil"""
    return jsonify({
        'message': 'Flask API - TP Docker',
        'endpoints': {
            'health': '/health',
            'init': 'POST /init',
            'users': 'GET /users',
            'create_user': 'POST /users'
        }
    }), 200
