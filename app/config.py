import psycopg2
import redis
from flask import current_app

def get_db_connection():
    """Créer une connexion PostgreSQL"""
    conn = psycopg2.connect(
        host=current_app.config['DB_HOST'],
        port=current_app.config['DB_PORT'],
        database=current_app.config['DB_NAME'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD']
    )
    return conn

def get_redis_client():
    """Créer un client Redis"""
    return redis.Redis(
        host=current_app.config['REDIS_HOST'],
        port=current_app.config['REDIS_PORT'],
        decode_responses=True
    )
