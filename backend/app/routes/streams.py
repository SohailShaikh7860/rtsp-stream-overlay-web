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

    return send_from_directory(stream_dir, filename)
