"""
RTSP stream conversion routes
"""
from flask import Blueprint, jsonify, request, send_from_directory
from app.services import stream_service

stream_bp = Blueprint("streams", __name__)


@stream_bp.route("/api/streams", methods=["POST"])
def create_stream():
    data = request.get_json()
    rtsp_url = data.get("rtsp_url") if data else None

    if not rtsp_url:
        return jsonify({"error": "Missing required field: rtsp_url"}), 400

    try:
        stream_id, _playlist_path = stream_service.start_stream(rtsp_url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not stream_service.wait_for_playlist(stream_id):
        log_path = stream_service.get_stream_log_path(stream_id)
        stream_service.stop_stream(stream_id)
        return (
            jsonify(
                {
                    "error": "Stream failed to start. Check RTSP URL.",
                    "log_path": str(log_path) if log_path else None,
                }
            ),
            500,
        )

    base_url = request.host_url.rstrip("/")
    hls_url = f"{base_url}/streams/{stream_id}/index.m3u8"
    return jsonify({"id": stream_id, "hls_url": hls_url}), 201


@stream_bp.route("/api/streams/<stream_id>", methods=["DELETE"])
def delete_stream(stream_id):
    success = stream_service.stop_stream(stream_id)
    if success:
        return jsonify({"message": "Stream stopped"}), 200
    return jsonify({"error": "Stream not found"}), 404


@stream_bp.route("/streams/<stream_id>/<path:filename>")
def serve_stream_file(stream_id, filename):
    stream_dir = stream_service.get_stream_dir(stream_id)
    if not stream_dir:
        return jsonify({"error": "Stream not found"}), 404

    response = send_from_directory(stream_dir, filename)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    if filename.endswith('.m3u8'):
        response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    elif filename.endswith('.ts'):
        response.headers['Content-Type'] = 'video/mp2t'
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    
    return response
