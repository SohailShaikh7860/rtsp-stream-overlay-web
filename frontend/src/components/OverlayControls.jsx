function OverlayControls({
  newOverlayType,
  newOverlayText,
  newOverlayImage,
  setNewOverlayType,
  setNewOverlayText,
  setNewOverlayImage,
  onCreateOverlay,
  selectedOverlay,
  onUpdateOverlay,
  onRemoveOverlay,
  overlays,
  selectedId,
  setSelectedId,
}) {
  const handleOverlayTypeChange = (event) => {
    setNewOverlayType(event.target.value)
  }

  const handleOverlayTextChange = (event) => {
    setNewOverlayText(event.target.value)
  }

  const handleOverlayImageChange = (event) => {
    setNewOverlayImage(event.target.value)
  }

  return (
    <section className="card">
      <h2>Overlay Controls</h2>
      <div className="stack">
        <label className="field">
          <span>Overlay Type</span>
          <select value={newOverlayType} onChange={handleOverlayTypeChange}>
            <option value="text">Text</option>
            <option value="image">Image / Logo</option>
          </select>
        </label>
        {newOverlayType === 'text' ? (
          <label className="field">
            <span>Text Content</span>
            <input
              type="text"
              value={newOverlayText}
              onChange={handleOverlayTextChange}
              placeholder="Breaking news..."
            />
          </label>
        ) : (
          <label className="field">
            <span>Image URL</span>
            <input
              type="text"
              value={newOverlayImage}
              onChange={handleOverlayImageChange}
              placeholder="https://example.com/logo.png"
            />
          </label>
        )}
        <button className="primary" onClick={onCreateOverlay}>
          Add Overlay
        </button>
      </div>

      {selectedOverlay && (
        <div className="editor">
          <h3>Selected Overlay</h3>
          <div className="stack">
            <label className="field">
              <span>Content</span>
              <input
                type="text"
                value={selectedOverlay.content}
                onChange={(event) =>
                  onUpdateOverlay(selectedOverlay.id, {
                    content: event.target.value,
                  })
                }
              />
            </label>
            {selectedOverlay.type === 'text' && (
              <>
                <label className="field">
                  <span>Text Color</span>
                  <input
                    type="color"
                    value={selectedOverlay.style.color}
                    onChange={(event) =>
                      onUpdateOverlay(selectedOverlay.id, {
                        style: {
                          ...selectedOverlay.style,
                          color: event.target.value,
                        },
                      })
                    }
                  />
                </label>
                <label className="field">
                  <span>Font Size</span>
                  <input
                    type="number"
                    min="10"
                    max="64"
                    value={selectedOverlay.style.fontSize}
                    onChange={(event) =>
                      onUpdateOverlay(selectedOverlay.id, {
                        style: {
                          ...selectedOverlay.style,
                          fontSize: Number(event.target.value),
                        },
                      })
                    }
                  />
                </label>
              </>
            )}
            <button
              className="ghost"
              onClick={() => onRemoveOverlay(selectedOverlay.id)}
            >
              Remove Overlay
            </button>
          </div>
        </div>
      )}

      <div className="overlay-list">
        <h3>Active Overlays</h3>
        {overlays.length === 0 ? (
          <p className="helper">No overlays yet.</p>
        ) : (
          overlays.map((overlay) => (
            <button
              key={overlay.id}
              className={`overlay-pill ${overlay.id === selectedId ? 'active' : ''}`}
              onClick={() => setSelectedId(overlay.id)}
            >
              {overlay.type === 'text' ? 'Text' : 'Image'}: {overlay.content}
            </button>
          ))
        )}
      </div>
    </section>
  )
}

export default OverlayControls
