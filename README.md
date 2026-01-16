# RTSP Web Application

A full-stack web application for streaming RTSP video feeds with real-time overlay management. Convert RTSP streams to HLS for web playback and add customizable text and image overlays with drag-and-drop functionality.

## Features

- **RTSP to HLS Conversion**: Convert RTSP streams to HLS format for web browser playback
- **Dynamic Overlays**: Add, edit, and manage text and image overlays on live streams
- **Drag & Drop Interface**: Intuitive overlay positioning with visual controls
- **Database Persistence**: Overlay configurations saved to MongoDB
- **Real-time Updates**: Live stream playback with HLS.js
- **RESTful API**: Complete CRUD operations for overlays and streams

## Tech Stack

**Frontend:** React 19.2.0, Vite 7.2.4, HLS.js 1.6.15

**Backend:** Flask 3.0.0, MongoDB (PyMongo), FFmpeg

## Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- FFmpeg - [Download here](https://ffmpeg.org/download.html)
- MongoDB Atlas Account - [Sign up here](https://www.mongodb.com/cloud/atlas)

## Quick Setup

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in `backend` directory:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the app at: **http://localhost:5173**

## How to Set Up RTSP Stream (Windows)

### Step 1: Download and Install FFmpeg

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the zip file to `C:\ffmpeg`
3. Add to PATH:
   - Open "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add `C:\ffmpeg\bin`
   - Restart your terminal
4. Verify installation:
   ```bash
   ffmpeg -version
   ```

### Step 2: Download MediaMTX (RTSP Server)

1. Download from [MediaMTX Releases](https://github.com/bluenviron/mediamtx/releases)
2. Download `mediamtx_vX.X.X_windows_amd64.zip`
3. Extract to a folder (e.g., `C:\mediamtx`)

### Step 3: Start MediaMTX Server

Open Command Prompt or PowerShell in the MediaMTX folder:
```bash
mediamtx.exe
```

You should see:
```
INF MediaMTX v1.x.x
INF listener opened on :8554 (RTSP)
INF listener opened on :1935 (RTMP)
INF listener opened on :8888 (HLS)
```

**Keep this terminal running!**

### Step 4: Stream Video to MediaMTX

Open a **new** Command Prompt/PowerShell window.

**Option A: Stream Your Webcam**

First, find your camera name:
```bash
ffmpeg -list_devices true -f dshow -i dummy
```

Then stream it:
```bash
ffmpeg -f dshow -i video="YOUR_CAMERA_NAME" -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://localhost:8554/mystream
```

Example:
```bash
ffmpeg -f dshow -i video="Integrated Camera" -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://localhost:8554/mystream
```

**Option B: Stream a Video File**

```bash
ffmpeg -re -stream_loop -1 -i "C:\path\to\video.mp4" -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://localhost:8554/mystream
```

**Keep this terminal running!**

### Step 5: Use the RTSP URL in the Application

Your RTSP URL is now: `rtsp://localhost:8554/mystream`

1. Go to http://localhost:5173
2. Paste the RTSP URL: `rtsp://localhost:8554/mystream`
3. Click "Start RTSP Stream"
4. The video will start playing!

**Quick Summary:**
- **Terminal 1:** Run `mediamtx.exe`
- **Terminal 2:** Run FFmpeg streaming command
- **Terminal 3:** Run backend `python app.py`
- **Terminal 4:** Run frontend `npm run dev`
- **Browser:** Open http://localhost:5173 and use RTSP URL

## Using the Application

### Managing Overlays

**Create:** Select type (Text/Image), enter content, click "Create Overlay"

**Edit:** Click overlay, modify properties in control panel (auto-saves to database)

**Move:** Click and drag the overlay

**Resize:** Drag the resize handle (bottom-right corner)

**Delete:** Select overlay, click "Remove" button

### Playback Controls

Use play/pause, seek bar, and volume controls at the bottom of the video player.

## API Endpoints

Base URL: `http://localhost:5000`

### Stream Endpoints

- `POST /api/streams` - Start RTSP stream (requires `rtsp_url` in body)
- `DELETE /api/streams/{stream_id}` - Stop stream
- `GET /streams/{stream_id}/index.m3u8` - Access HLS playlist

### Overlay Endpoints

- `GET /api/overlays` - Get all overlays
- `GET /api/overlays/{id}` - Get single overlay
- `POST /api/overlays` - Create overlay (requires `type`, `content`)
- `PUT /api/overlays/{id}` - Update overlay
- `DELETE /api/overlays/{id}` - Delete overlay

**Example - Create Text Overlay:**
```bash
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{"type": "text", "content": "Live Stream", "style": {"color": "#ffffff", "fontSize": 20}}'
```

## Troubleshooting

**FFmpeg not recognized:**
- Ensure FFmpeg is added to PATH
- Restart terminal after adding to PATH
- Verify: `ffmpeg -version`

**MongoDB connection failed:**
- Check `MONGODB_URI` in `.env` file
- Whitelist your IP in MongoDB Atlas
- Verify database user permissions

**Stream not playing:**
- Ensure MediaMTX is running
- Check FFmpeg streaming terminal for errors
- Verify RTSP URL format is correct
- Confirm backend is running without errors

**MediaMTX port already in use:**
- Close other instances of MediaMTX
- Check if port 8554 is being used by another application

**Overlays not saving:**
- Verify MongoDB connection in backend logs
- Check browser console for API errors
- Ensure `.env` file exists with valid URI

## Demo Video

https://youtu.be/qRZnPrajLOM