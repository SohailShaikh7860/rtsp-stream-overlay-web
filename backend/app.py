from flask import jsonify
from app import create_app
from app.routes.overlays import overlay_bp

# Create Flask app
app = create_app()

# Register blueprints (routes)
app.register_blueprint(overlay_bp)

@app.route("/")
def home():
    return jsonify({
        "message": "Flask Backend is running!",
        "endpoints": {
            "ping": "/ping",
            "get_all_overlays": "GET /api/overlays",
            "create_overlay": "POST /api/overlays",
            "get_overlay": "GET /api/overlays/<id>",
            "update_overlay": "PUT /api/overlays/<id>",
            "delete_overlay": "DELETE /api/overlays/<id>"
        }
    })

@app.route("/ping")
def ping():
    return jsonify({"message": "pong", "status": "success"})

if __name__ == "__main__":
    print("=" * 50)
    print("Flask server starting...")
    print("Visit: http://127.0.0.1:5000/")
    print("Test endpoints:")
    print("  GET  http://127.0.0.1:5000/api/overlays")
    print("  POST http://127.0.0.1:5000/api/overlays")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)