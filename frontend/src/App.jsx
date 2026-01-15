import { useEffect, useMemo, useRef, useState } from 'react'
import Hls from 'hls.js'
import OverlayControls from './components/OverlayControls.jsx'
import PlaybackControls from './components/PlaybackControls.jsx'
import VideoStage from './components/VideoStage.jsx'

const BACKEND_URL = 'http://127.0.0.1:5000'
const MIN_OVERLAY_SIZE = 40

function App() {
  const videoRef = useRef(null)
  const stageRef = useRef(null)
  const hlsRef = useRef(null)
  const interactionRef = useRef(null)

  const [rtspUrl, setRtspUrl] = useState('rtsp://')
  const [hlsUrl, setHlsUrl] = useState('')
  const [videoUrl, setVideoUrl] = useState('')
  const [streamId, setStreamId] = useState(null)
  const [streamStatus, setStreamStatus] = useState('idle')
  const [streamError, setStreamError] = useState('')
  const [canPlay, setCanPlay] = useState(false)

  const [overlays, setOverlays] = useState([])
  const [selectedId, setSelectedId] = useState(null)

  const [newOverlayType, setNewOverlayType] = useState('text')
  const [newOverlayText, setNewOverlayText] = useState('Live')
  const [newOverlayImage, setNewOverlayImage] = useState('')

  const selectedOverlay = useMemo(
    () => overlays.find((overlay) => overlay.id === selectedId),
    [overlays, selectedId],
  )

  useEffect(() => {
    const handlePointerMove = (event) => {
      const interaction = interactionRef.current
      if (!interaction || !stageRef.current) {
        return
      }

      const rect = stageRef.current.getBoundingClientRect()
      const deltaX = event.clientX - interaction.startX
      const deltaY = event.clientY - interaction.startY

      setOverlays((prev) =>
        prev.map((overlay) => {
          if (overlay.id !== interaction.id) {
            return overlay
          }

          if (interaction.type === 'drag') {
            const maxX = Math.max(0, rect.width - overlay.width)
            const maxY = Math.max(0, rect.height - overlay.height)
            const nextX = Math.min(Math.max(0, interaction.originX + deltaX), maxX)
            const nextY = Math.min(Math.max(0, interaction.originY + deltaY), maxY)
            return { ...overlay, x: nextX, y: nextY }
          }

          const maxWidth = Math.max(MIN_OVERLAY_SIZE, rect.width - overlay.x)
          const maxHeight = Math.max(MIN_OVERLAY_SIZE, rect.height - overlay.y)
          const nextWidth = Math.min(
            Math.max(MIN_OVERLAY_SIZE, interaction.originWidth + deltaX),
            maxWidth,
          )
          const nextHeight = Math.min(
            Math.max(MIN_OVERLAY_SIZE, interaction.originHeight + deltaY),
            maxHeight,
          )
          return { ...overlay, width: nextWidth, height: nextHeight }
        }),
      )
    }

    const handlePointerUp = () => {
      interactionRef.current = null
    }

    window.addEventListener('pointermove', handlePointerMove)
    window.addEventListener('pointerup', handlePointerUp)
    return () => {
      window.removeEventListener('pointermove', handlePointerMove)
      window.removeEventListener('pointerup', handlePointerUp)
    }
  }, [])

  useEffect(() => {
    const video = videoRef.current
    if (!video || !videoUrl) {
      return
    }

    setStreamError('')
    setCanPlay(false)

    if (hlsRef.current) {
      hlsRef.current.destroy()
      hlsRef.current = null
    }

    const handleVideoError = (event) => {
      const error = video.error
      const errorDetails = {
        code: error?.code,
        message: error?.message,
        type: error?.code === 1 ? 'MEDIA_ERR_ABORTED' :
              error?.code === 2 ? 'MEDIA_ERR_NETWORK' :
              error?.code === 3 ? 'MEDIA_ERR_DECODE' :
              error?.code === 4 ? 'MEDIA_ERR_SRC_NOT_SUPPORTED' : 'UNKNOWN',
        videoUrl,
        videoSrc: video.src,
      }
      console.error('Video element error:', errorDetails)
      
      const errorMsg = error
        ? `Video error (${errorDetails.type}): ${error.message || 'Code ' + error.code}`
        : 'Video playback failed.'
      setStreamError(errorMsg)
      setCanPlay(false)
    }

    video.addEventListener('error', handleVideoError)

    if (Hls.isSupported()) {
      const hls = new Hls({
        debug: false,
        enableWorker: true,
        lowLatencyMode: false,
        backBufferLength: 90,
        maxBufferLength: 30,
        maxMaxBufferLength: 60,
        maxBufferSize: 60 * 1000 * 1000,
        maxBufferHole: 0.5,
        highBufferWatchdogPeriod: 2,
        nudgeOffset: 0.1,
        nudgeMaxRetry: 3,
        maxFragLookUpTolerance: 0.25,
        liveSyncDurationCount: 3,
        liveMaxLatencyDurationCount: 10,
        manifestLoadingTimeOut: 10000,
        manifestLoadingMaxRetry: 3,
        levelLoadingTimeOut: 10000,
        levelLoadingMaxRetry: 3,
        fragLoadingTimeOut: 20000,
        fragLoadingMaxRetry: 3,
      })
      
      hls.on(Hls.Events.ERROR, (_event, data) => {

        if (data.fatal || data.details !== 'bufferStalledError') {
          console.error('HLS.js error:', {
            type: data.type,
            details: data.details,
            fatal: data.fatal,
            error: data.error,
            url: data.url,
          })
        }
        
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              console.log('Network error, attempting recovery...')
              setStreamError(`Network error: ${data.details}`)
              hls.startLoad()
              break
            case Hls.ErrorTypes.MEDIA_ERROR:
              console.log('Media error, attempting recovery...')
              setStreamError(`Media error: ${data.details}`)
              hls.recoverMediaError()
              break
            default:
              setStreamError(
                `HLS Error: ${data.type} - ${data.details || 'Stream failed'}`,
              )
              setCanPlay(false)
              hls.destroy()
              break
          }
        }
      })
      
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        console.log('HLS manifest parsed successfully')
        setCanPlay(true)
        setStreamError('')
        video.play().catch((err) => {
          console.warn('Auto-play blocked:', err.message)
        })
      })
      
      hls.loadSource(videoUrl)
      hls.attachMedia(video)
      hlsRef.current = hls
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {

      console.log('Using native HLS support')
      video.src = videoUrl
      const handleLoaded = () => setCanPlay(true)
      video.addEventListener('loadedmetadata', handleLoaded)
      return () => {
        video.removeEventListener('error', handleVideoError)
        video.removeEventListener('loadedmetadata', handleLoaded)
      }
    } else {
      setStreamError('HLS playback is not supported in this browser.')
      setCanPlay(false)
    }

    return () => {
      video.removeEventListener('error', handleVideoError)
      if (hlsRef.current) {
        hlsRef.current.destroy()
        hlsRef.current = null
      }
    }
  }, [videoUrl])

  const handleCreateOverlay = () => {
    const trimmedText = newOverlayText.trim()
    const trimmedImage = newOverlayImage.trim()

    if (newOverlayType === 'text' && !trimmedText) {
      return
    }
    if (newOverlayType === 'image' && !trimmedImage) {
      return
    }

    const baseOverlay = {
      id: `${Date.now()}-${Math.round(Math.random() * 1000)}`,
      x: 24,
      y: 24,
      width: 180,
      height: 60,
      type: newOverlayType,
      content: newOverlayType === 'text' ? trimmedText : trimmedImage,
      style: {
        color: '#ffffff',
        fontSize: 18,
      },
    }

    setOverlays((prev) => [...prev, baseOverlay])
    setSelectedId(baseOverlay.id)
  }

  const handleRemoveOverlay = (overlayId) => {
    setOverlays((prev) => prev.filter((overlay) => overlay.id !== overlayId))
    if (selectedId === overlayId) {
      setSelectedId(null)
    }
  }

  const updateOverlay = (overlayId, updates) => {
    setOverlays((prev) =>
      prev.map((overlay) =>
        overlay.id === overlayId ? { ...overlay, ...updates } : overlay,
      ),
    )
  }

  const handleLoadHls = () => {
    if (!hlsUrl.trim()) {
      return
    }
    setStreamStatus('ready')
    setStreamError('')
    setVideoUrl(hlsUrl.trim())
  }

  const stopStream = async () => {
    if (!streamId) {
      return
    }
    try {
      await fetch(`${BACKEND_URL}/api/streams/${streamId}`, {
        method: 'DELETE',
      })
    } catch (error) {
      console.error(error)
    } finally {
      setStreamId(null)
      setStreamStatus('idle')
    }
  }

  const handleConvertAndPlay = async () => {
    if (!rtspUrl.trim()) {
      return
    }

    setStreamStatus('starting')
    setStreamError('')

    try {
      if (streamId) {
        await stopStream()
      }

      const response = await fetch(`${BACKEND_URL}/api/streams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rtsp_url: rtspUrl.trim() }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Unable to start stream')
      }

      const data = await response.json()
      setStreamId(data.id)
      setVideoUrl(data.hls_url)
      setStreamStatus('ready')
    } catch (error) {
      setStreamError(error.message || 'Unable to start stream')
      setStreamStatus('error')
    }
  }

  return (
    <>
      <div className="page">
        <header className="page-header">
          <div>
            <p className="eyebrow">RTSP Livestream Studio</p>
            <h1>RTSP Livestream with Overlays</h1>
            <p className="subtitle">
              Play RTSP feeds via backend conversion or a provided HLS URL, then
              layer text or image overlays on top.
            </p>
          </div>
        </header>

        <div className="content-grid">
          <div className="stack">
            <PlaybackControls
              rtspUrl={rtspUrl}
              hlsUrl={hlsUrl}
              setRtspUrl={setRtspUrl}
              setHlsUrl={setHlsUrl}
              onConvertAndPlay={handleConvertAndPlay}
              onLoadHls={handleLoadHls}
              videoRef={videoRef}
              onStopStream={stopStream}
              streamStatus={streamStatus}
              streamError={streamError}
              videoUrl={videoUrl}
              canPlay={canPlay}
            />

            <VideoStage
              videoRef={videoRef}
              stageRef={stageRef}
              overlays={overlays}
              selectedId={selectedId}
              interactionRef={interactionRef}
              setSelectedId={setSelectedId}
              videoUrl={videoUrl}
            />
          </div>

          <OverlayControls
            newOverlayType={newOverlayType}
            newOverlayText={newOverlayText}
            newOverlayImage={newOverlayImage}
            setNewOverlayType={setNewOverlayType}
            setNewOverlayText={setNewOverlayText}
            setNewOverlayImage={setNewOverlayImage}
            onCreateOverlay={handleCreateOverlay}
            selectedOverlay={selectedOverlay}
            onUpdateOverlay={updateOverlay}
            onRemoveOverlay={handleRemoveOverlay}
            overlays={overlays}
            selectedId={selectedId}
            setSelectedId={setSelectedId}
          />
        </div>
      </div>
    </>
  )
}

export default App
