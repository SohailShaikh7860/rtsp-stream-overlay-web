"""MongoDB database configuration and connection management."""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

_db = None
_client = None

def get_database():
    global _db, _client
    
    if _db is not None:
        return _db
    
    try:
        
        mongodb_uri = os.getenv('MONGODB_URI')
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is not set")
        
        
        _client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,  
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        _client.admin.command('ping')
        
        _db = _client.get_database()
        
        print(f"Successfully connected to MongoDB database: {_db.name}")
        return _db
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise ConnectionFailure("Unable to connect to MongoDB Atlas") from e
    except ValueError as e:
        print(f"Configuration error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error connecting to MongoDB: {e}")
        raise

def get_collection(collection_name):
    
    db = get_database()
    return db[collection_name]

def close_connection():
    """Close the MongoDB connection."""
    global _client, _db
    
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        print("MongoDB connection closed")
