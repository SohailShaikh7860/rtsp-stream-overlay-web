function VideoStage({
  videoRef,
  stageRef,
  overlays,
  selectedId,
  interactionRef,
  setSelectedId,
  videoUrl,
}) {
  const handleStagePointerDown = () => {
    setSelectedId(null)
  }

  const handleOverlayPointerDown = (event, overlay) => {
    event.stopPropagation()
    interactionRef.current = {
      type: 'drag',
      id: overlay.id,
      startX: event.clientX,
      startY: event.clientY,
      originX: overlay.x,
      originY: overlay.y,
    }
    setSelectedId(overlay.id)
  }

  const handleResizePointerDown = (event, overlay) => {
    event.stopPropagation()
    interactionRef.current = {
      type: 'resize',
      id: overlay.id,
      startX: event.clientX,
      startY: event.clientY,
      originWidth: overlay.width,
      originHeight: overlay.height,
    }
    setSelectedId(overlay.id)
  }

  return (
    <div className="video-stage" ref={stageRef} onPointerDown={handleStagePointerDown}>
      <video ref={videoRef} controls playsInline className="video-player" />
      <div className="overlay-layer">
        {overlays.map((overlay) => (
          <div
            key={overlay.id}
            className={`overlay-item ${selectedId === overlay.id ? 'selected' : ''}`}
            style={{
              left: overlay.x,
              top: overlay.y,
              width: overlay.width,
              height: overlay.height,
            }}
            onPointerDown={(event) => handleOverlayPointerDown(event, overlay)}
          >
            {overlay.type === 'text' ? (
              <div
                className="overlay-text"
                style={{
                  color: overlay.style.color,
                  fontSize: overlay.style.fontSize,
                }}
              >
                {overlay.content}
              </div>
            ) : (
              <img
                src={overlay.content}
                alt="Overlay"
                className="overlay-image"
                draggable={false}
              />
            )}
            <div
              className="resize-handle"
              onPointerDown={(event) => handleResizePointerDown(event, overlay)}
            />
          </div>
        ))}
      </div>
      {!videoUrl && (
        <div className="video-placeholder">
          <p>Load a stream to start playback.</p>
        </div>
      )}
    </div>
  )
}

export default VideoStage
