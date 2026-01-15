from flask import Flask
from flask_cors import CORS
from app.config.database import get_database

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)

    try:
        db = get_database()
        print(f"MongoDB initialized successfully - Database: {db.name}")
    except Exception as e:
        print(f"Warning: Could not initialize MongoDB: {e}")
        print("Application will continue without database persistence")
    
    return app
