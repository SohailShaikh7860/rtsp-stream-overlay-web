import shutil
import subprocess
import time
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
        "12",
        "-hls_flags",
        "append_list+omit_endlist",
        "-hls_segment_filename",
        str(stream_dir / "segment_%03d.ts"),
        str(playlist_path),
    ]

    log_path = stream_dir / "ffmpeg.log"
    log_file = log_path.open("w", encoding="utf-8")

    process = subprocess.Popen(
        command,
        stdout=log_file,
        stderr=log_file,
        stdin=subprocess.DEVNULL,
    )

    _streams[stream_id] = {
        "process": process,
        "dir": stream_dir,
        "log_file": log_file,
        "log_path": log_path,
    }

    return stream_id, playlist_path


def wait_for_playlist(stream_id, timeout=12, interval=0.25):

    stream = _streams.get(stream_id)
    if not stream:
        return False

    playlist_path = stream["dir"] / "index.m3u8"
    start_time = time.time()

    while time.time() - start_time < timeout:
        if playlist_path.exists() and playlist_path.stat().st_size > 0:
            return True
        if stream["process"].poll() is not None:
            return False
        time.sleep(interval)

    return playlist_path.exists() and playlist_path.stat().st_size > 0


def stop_stream(stream_id):
    """Stop an active stream and remove generated files."""
    stream = _streams.get(stream_id)
    if not stream:
        return False

    process = stream["process"]
    if process.poll() is None:
        process.terminate()

    if stream.get("log_file"):
        stream["log_file"].close()

    shutil.rmtree(stream["dir"], ignore_errors=True)
    _streams.pop(stream_id, None)
    return True


def get_stream_log_path(stream_id):
    """Return the log path for debugging."""
    stream = _streams.get(stream_id)
    if stream:
        return stream.get("log_path")
    return None


def get_stream_dir(stream_id):
    """Return the stream directory for the given ID."""
    stream = _streams.get(stream_id)
    if stream:
        return stream["dir"]


    stream_dir = STREAM_ROOT / stream_id
    if stream_dir.exists():
        return stream_dir
    return None
