_overlays = []
_next_id = 1

def get_all_overlays():
    """Get all overlays"""
    return _overlays.copy()

def get_overlay_by_id(overlay_id):
    """Get a single overlay by ID"""
    for overlay in _overlays:
        if overlay['id'] == overlay_id:
            return overlay
    return None

def create_overlay(overlay_data):
    """Create a new overlay"""
    global _next_id
    
    new_overlay = {
        'id': _next_id,
        'type': overlay_data.get('type'), 
        'content': overlay_data.get('content'),  
        'position': overlay_data.get('position', {'x': 0, 'y': 0}),
        'size': overlay_data.get('size', {'width': 100, 'height': 50}),
        'style': overlay_data.get('style', {})
    }
    
    _overlays.append(new_overlay)
    _next_id += 1
    return new_overlay

def update_overlay(overlay_id, overlay_data):
    """Update an existing overlay"""
    overlay = get_overlay_by_id(overlay_id)
    if not overlay:
        return None
    
    # Update only provided fields
    if 'type' in overlay_data:
        overlay['type'] = overlay_data['type']
    if 'content' in overlay_data:
        overlay['content'] = overlay_data['content']
    if 'position' in overlay_data:
        overlay['position'] = overlay_data['position']
    if 'size' in overlay_data:
        overlay['size'] = overlay_data['size']
    if 'style' in overlay_data:
        overlay['style'] = overlay_data['style']
    
    return overlay

def delete_overlay(overlay_id):
    """Delete an overlay"""
    global _overlays
    overlay = get_overlay_by_id(overlay_id)
    if overlay:
        _overlays = [o for o in _overlays if o['id'] != overlay_id]
        return True
    return False
