import shutil
import subprocess
import uuid
from pathlib import Path

STREAM_ROOT = Path(__file__).resolve().parents[2] / "streams"
STREAM_ROOT.mkdir(parents=True, exist_ok=True)

_streams = {}


def start_stream(rtsp_url):
    """Start an RTSP -> HLS conversion via ffmpeg."""
    if not shutil.which("ffmpeg"):
        raise ValueError("ffmpeg is not installed or not on PATH.")

    stream_id = uuid.uuid4().hex[:10]
    stream_dir = STREAM_ROOT / stream_id
    stream_dir.mkdir(parents=True, exist_ok=True)

    playlist_path = stream_dir / "index.m3u8"

    command = [
        "ffmpeg",
        "-rtsp_transport",
        "tcp",
        "-i",
        rtsp_url,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-tune",
        "zerolatency",
        "-c:a",
        "aac",
        "-f",
        "hls",
        "-hls_time",
        "2",
        "-hls_list_size",
        "6",
        "-hls_flags",
        "delete_segments+append_list",
        "-hls_segment_filename",
        str(stream_dir / "segment_%03d.ts"),
        str(playlist_path),
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )

    _streams[stream_id] = {
        "process": process,
        "dir": stream_dir,
    }

    return stream_id, playlist_path


def stop_stream(stream_id):
    """Stop an active stream and remove generated files."""
    stream = _streams.get(stream_id)
    if not stream:
        return False

    process = stream["process"]
    if process.poll() is None:
        process.terminate()

    shutil.rmtree(stream["dir"], ignore_errors=True)
    _streams.pop(stream_id, None)
    return True


def get_stream_dir(stream_id):
    """Return the stream directory for the given ID."""
    stream = _streams.get(stream_id)
    if not stream:
        return None
    return stream["dir"]
