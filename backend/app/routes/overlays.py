"""
Overlay CRUD API routes
"""
from flask import Blueprint, request, jsonify
from app.services import overlay_service

# Create a Blueprint (like a mini Flask app for routes)
overlay_bp = Blueprint('overlays', __name__)

@overlay_bp.route('/api/overlays', methods=['GET'])
def get_overlays():
    """Get all overlays"""
    overlays = overlay_service.get_all_overlays()
    return jsonify(overlays)

@overlay_bp.route('/api/overlays/<overlay_id>', methods=['GET'])
def get_overlay(overlay_id):
    """Get a single overlay by ID"""
    overlay = overlay_service.get_overlay_by_id(overlay_id)
    if overlay:
        return jsonify(overlay)
    return jsonify({'error': 'Overlay not found'}), 404

@overlay_bp.route('/api/overlays', methods=['POST'])
def create_overlay():
    """Create a new overlay"""
    data = request.get_json()
    
    # Basic validation
    if not data or 'type' not in data or 'content' not in data:
        return jsonify({'error': 'Missing required fields: type, content'}), 400
    
    overlay = overlay_service.create_overlay(data)
    return jsonify(overlay), 201

@overlay_bp.route('/api/overlays/<overlay_id>', methods=['PUT'])
def update_overlay(overlay_id):
    """Update an existing overlay"""
    data = request.get_json()
    
    overlay = overlay_service.update_overlay(overlay_id, data)
    if overlay:
        return jsonify(overlay)
    return jsonify({'error': 'Overlay not found'}), 404

@overlay_bp.route('/api/overlays/<overlay_id>', methods=['DELETE'])
def delete_overlay(overlay_id):
    """Delete an overlay"""
    success = overlay_service.delete_overlay(overlay_id)
    if success:
        return jsonify({'message': 'Overlay deleted successfully'})
    return jsonify({'error': 'Overlay not found'}), 404
