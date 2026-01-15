function PlaybackControls({
  rtspUrl,
  hlsUrl,
  setRtspUrl,
  setHlsUrl,
  onConvertAndPlay,
  onLoadHls,
  videoRef,
  onStopStream,
  streamStatus,
  streamError,
  videoUrl,
  canPlay,
}) {
  const handleRtspChange = (event) => {
    setRtspUrl(event.target.value)
  }


  const handlePlay = () => {
    if (videoRef?.current && videoUrl) {
      videoRef.current.play()
    }
  }

  const handlePause = () => {
    if (videoRef?.current && videoUrl) {
      videoRef.current.pause()
    }
  }

  const isReady = Boolean(videoUrl) && canPlay

  return (
    <section className="card">
      <h2>Livestream Playback</h2>
      <div className="stack">
        <label className="field">
          <span>RTSP URL</span>
          <input
            type="text"
            value={rtspUrl}
            onChange={handleRtspChange}
            placeholder="rtsp://your-stream-url"
          />
        </label>
        <button className="primary" onClick={onConvertAndPlay}>
          Convert RTSP &amp; Play
        </button>


        <div className="button-row">
          <button onClick={handlePlay} disabled={!isReady}>
            Play
          </button>
          <button onClick={handlePause} disabled={!isReady}>
            Pause
          </button>
          <button className="ghost" onClick={onStopStream}>
            Stop Stream
          </button>
        </div>

        <div className="status">
          <span>Status: {streamStatus}</span>
          {streamError && <span className="error">{streamError}</span>}
        </div>
        <p className="helper">
          Tip: Use RTSP.me or any RTSP gateway to generate a temporary RTSP
          stream. The backend uses ffmpeg to convert RTSP to HLS.
        </p>
      </div>
    </section>
  )
}

export default PlaybackControls
