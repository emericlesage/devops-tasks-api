from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['DB_HOST'] = os.getenv('DB_HOST', 'localhost')
    app.config['DB_PORT'] = os.getenv('DB_PORT', '5432')
    app.config['DB_NAME'] = os.getenv('DB_NAME', 'flask_db')
    app.config['DB_USER'] = os.getenv('DB_USER', 'flask_user')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'supersecret')
    app.config['REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
    app.config['REDIS_PORT'] = int(os.getenv('REDIS_PORT', '6379'))
    
    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app

# Créer l'instance pour Flask CLI
app = create_app()
