from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)
    
    return app
