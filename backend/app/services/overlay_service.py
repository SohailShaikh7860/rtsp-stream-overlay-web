"""Overlay service - MongoDB implementation"""
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from app.config.database import get_collection

def _serialize_overlay(overlay):
    """Convert MongoDB document to JSON-serializable format"""
    if overlay and '_id' in overlay:
        overlay['id'] = str(overlay['_id'])
        del overlay['_id']
    return overlay

def get_all_overlays():
    """Get all overlays from MongoDB"""
    try:
        collection = get_collection('overlays')
        overlays = list(collection.find())
        return [_serialize_overlay(overlay) for overlay in overlays]
    except Exception as e:
        print(f"Error fetching overlays: {e}")
        return []

def get_overlay_by_id(overlay_id):
    """Get a single overlay by ID from MongoDB"""
    try:
        collection = get_collection('overlays')
        overlay = collection.find_one({'_id': ObjectId(overlay_id)})
        return _serialize_overlay(overlay) if overlay else None
    except (InvalidId, Exception) as e:
        print(f"Error fetching overlay {overlay_id}: {e}")
        return None

def create_overlay(overlay_data):
    """Create a new overlay in MongoDB"""
    try:
        collection = get_collection('overlays')
        
        new_overlay = {
            'name': overlay_data.get('name', 'Untitled'),
            'type': overlay_data.get('type'),
            'content': overlay_data.get('content'),
            'position': overlay_data.get('position', {'x': 0, 'y': 0}),
            'size': overlay_data.get('size', {'width': 100, 'height': 50}),
            'style': overlay_data.get('style', {}),
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        result = collection.insert_one(new_overlay)
        
        created_overlay = collection.find_one({'_id': result.inserted_id})
        return _serialize_overlay(created_overlay)
    except Exception as e:
        print(f"Error creating overlay: {e}")
        return None

def update_overlay(overlay_id, overlay_data):
    """Update an existing overlay in MongoDB"""
    try:
        collection = get_collection('overlays')
        
        # Prepare update data
        update_fields = {}
        if 'name' in overlay_data:
            update_fields['name'] = overlay_data['name']
        if 'type' in overlay_data:
            update_fields['type'] = overlay_data['type']
        if 'content' in overlay_data:
            update_fields['content'] = overlay_data['content']
        if 'position' in overlay_data:
            update_fields['position'] = overlay_data['position']
        if 'size' in overlay_data:
            update_fields['size'] = overlay_data['size']
        if 'style' in overlay_data:
            update_fields['style'] = overlay_data['style']
        
        
        update_fields['updatedAt'] = datetime.utcnow()
        
        
        result = collection.update_one(
            {'_id': ObjectId(overlay_id)},
            {'$set': update_fields}
        )
        
        if result.matched_count == 0:
            return None
        

        updated_overlay = collection.find_one({'_id': ObjectId(overlay_id)})
        return _serialize_overlay(updated_overlay)
    except (InvalidId, Exception) as e:
        print(f"Error updating overlay {overlay_id}: {e}")
        return None

def delete_overlay(overlay_id):
    """Delete an overlay from MongoDB"""
    try:
        collection = get_collection('overlays')
        result = collection.delete_one({'_id': ObjectId(overlay_id)})
        return result.deleted_count > 0
    except (InvalidId, Exception) as e:
        print(f"Error deleting overlay {overlay_id}: {e}")
        return False
