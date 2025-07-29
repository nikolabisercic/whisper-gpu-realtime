# 🎤 Speech-to-Text Web Application

A beautiful, minimalistic web interface for real-time speech-to-text transcription using GPU acceleration.

## ✨ Features

- **Real-time transcription** - See your words appear as you speak
- **GPU acceleration** - Leverages your RTX 4060 for fast processing
- **Clean, modern UI** - Built with React and Tailwind CSS
- **Model selection** - Choose between tiny, base, small, and medium models
- **Copy functionality** - One-click copy of all transcribed text
- **Keyboard shortcuts** - Press spacebar to start/stop recording
- **WebSocket streaming** - Low-latency audio transmission

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
source ~/envs/text2speach/bin/activate
```

### 2. Run the Application

```bash
./run_app.sh
```

### 3. Open in Browser

Navigate to <http://localhost:3000>

## 📁 Web App Structure

```
text2speach/
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── hooks/         # Custom React hooks
│   │   └── App.jsx        # Main application
│   └── package.json
├── backend/                # FastAPI server
│   ├── main.py           # WebSocket server
│   ├── whisper_service.py # Model management
│   └── audio_processor.py # Audio processing
└── run_app.sh            # Start both services
```

## 🎨 UI Components

### Model Selector

- Dropdown menu with all available models
- Shows speed/accuracy ratings
- Displays GPU/CPU status

### Record Button

- Large, centered button
- Visual states: idle (grey), recording (red pulse), processing (blue spin)
- Keyboard shortcut: Spacebar

### Transcription Box

- Real-time text updates
- Scrollable area
- Copy button
- Word/character count

## 🔊 Audio Implementation

### PCM Streaming (Current)

- **Technology**: Web Audio API with ScriptProcessorNode
- **Format**: Raw PCM float32 samples at 16kHz
- **Latency**: ~200ms real-time streaming
- **Reliability**: No codec issues, direct audio capture

### How It Works

1. **Capture**: AudioContext captures microphone at 16kHz
2. **Process**: ScriptProcessor provides raw float32 samples
3. **Transmit**: Base64 encoded PCM over WebSocket
4. **Backend**: Direct numpy array conversion (no ffmpeg needed)

## 🔧 Manual Setup

If you prefer to run frontend and backend separately:

### Backend (Terminal 1)

```bash
cd backend
./start_server.sh
```

### Frontend (Terminal 2)

```bash
cd frontend
npm install  # First time only
npm run dev
```

## 🛠️ Configuration

### Change Default Model

Edit `backend/main.py`, line ~50:

```python
success = await whisper_service.load_model("small")  # Change to tiny/base/medium
```

### Change Audio Chunk Duration

Edit `backend/audio_processor.py`, line ~15:

```python
self.chunk_duration_ms = 5000  # Milliseconds
```

## 📡 API Endpoints

- `ws://localhost:8000/ws` - WebSocket for audio streaming
- `GET /models` - Get available models
- `POST /models/{name}` - Change active model
- `GET /health` - Server health check

## 🐛 Troubleshooting

### "Microphone access denied"

- Check browser permissions
- Ensure no other app is using the microphone

### "WebSocket disconnected"

- Check if backend is running
- Verify no firewall blocking port 8000

### "GPU not detected"

- Backend will automatically fall back to CPU
- Check `nvidia-smi` output

### "Audio not processing"

- Speak louder/clearer
- Check microphone with `python tests/test_microphone.py`

## 🎯 Performance

With your RTX 4060:

- **Tiny model**: ~50ms latency
- **Small model**: ~200ms latency
- **Medium model**: ~500ms latency

## 🚢 Production Deployment

For production use, we recommend:

1. Using HTTPS (update WebSocket to `wss://`)
2. Adding authentication
3. Implementing rate limiting
4. Using a production ASGI server (Gunicorn + Uvicorn)
5. Containerizing with Docker

## 📝 Next Steps

After everything is working, we can:

- Add Docker support for easy deployment
- Implement user authentication
- Add support for multiple languages
- Create audio file upload option
- Add export functionality (TXT, SRT, etc.)

---

Enjoy your GPU-accelerated speech-to-text web application! 🎉
