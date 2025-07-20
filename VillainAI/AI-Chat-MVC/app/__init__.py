from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.controllers.chat_controller import chat_bp
    app.register_blueprint(chat_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app