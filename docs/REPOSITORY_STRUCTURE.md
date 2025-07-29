# 📁 Repository Structure

```
text2speach/
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md               # 2-minute setup guide
├── 📄 TROUBLESHOOTING.md          # Common issues & solutions
├── 📄 .env.example                # Environment template
├── 📄 .env                        # Your local config (git ignored)
├── 📄 .gitignore                  # Git ignore rules
├── 📄 docker-compose.yml          # Docker orchestration
├── 📄 docker-compose.dev.yml      # Development overrides
│
├── 🎨 frontend/                   # React web interface
│   ├── 📄 package.json           # Node dependencies
│   ├── 📄 vite.config.js         # Vite configuration
│   ├── 📄 nginx.conf             # Production server config
│   ├── 📄 Dockerfile             # Frontend container
│   ├── 📄 Dockerfile.dev         # Development container
│   ├── 📁 public/               # Static assets
│   └── 📁 src/                  # React source code
│       ├── 📄 App.jsx           # Main application
│       ├── 📄 index.css         # Tailwind styles
│       ├── 📁 components/       # UI components
│       │   ├── ModelSelector.jsx
│       │   ├── RecordButton.jsx
│       │   ├── TranscriptionBox.jsx
│       │   └── StatusIndicator.jsx
│       └── 📁 hooks/            # React hooks
│           ├── useWebSocket.js      # WebSocket connection
│           ├── useAudioRecorder.js  # Original WebM recorder
│           └── useAudioRecorderPCM.js # PCM streaming (active)
│
├── 🔧 backend/                    # FastAPI server
│   ├── 📄 main.py                # API & WebSocket server
│   ├── 📄 whisper_service.py     # Whisper model management
│   ├── 📄 audio_processor.py     # Audio processing (PCM/WebM)
│   ├── 📄 requirements.txt       # Python dependencies
│   ├── 📄 start_server.sh        # Backend launcher script
│   └── 📄 Dockerfile             # Backend container
│
├── 🐍 src/                       # Original CLI implementation
│   └── 📄 speech_to_text.py     # Command-line version
│
├── 📜 scripts/                    # Launcher & utility scripts
│   ├── 📄 run_app.sh            # Web app launcher
│   ├── 📄 run.py                # CLI launcher
│   ├── 📄 gpu_speech.sh         # GPU-enabled launcher
│   ├── 📄 gpu_launcher.sh       # CUDA library setup
│   ├── 📄 download_models.py    # Model downloader
│   ├── 📄 launch_gpu.py         # GPU launch utility
│   ├── 📄 run_speech_to_text.sh # Speech script runner
│   ├── 📄 run_stt.sh            # STT runner
│   └── 📄 start.py              # Start utility
│
├── 🧪 tests/                     # Test files
│   ├── 📄 test_gpu_simple.py    # GPU verification
│   ├── 📄 test_gpu_transcription.py # Transcription test
│   ├── 📄 test_faster_whisper.py # Whisper tests
│   ├── 📄 test_microphone.py    # Audio capture test
│   ├── 📄 test_nvidia.py        # NVIDIA library test
│   ├── 📄 test_pytorch_cuda.py  # PyTorch CUDA test
│   └── 📄 test_whisper_simple.py # Basic Whisper test
│
├── 📋 docs/                      # Additional documentation
│   ├── 📄 REPOSITORY_STRUCTURE.md # This file
│   ├── 📄 WEB_APP_README.md     # Web app details
│   ├── 📄 PCM_STREAMING_UPDATE.md # Audio implementation
│   └── 📄 DEPRECATION_FIXES.md  # Docker/API updates
│
├── 📁 recordings/                # Audio recordings (git ignored)
│   └── test_recording.wav       # Sample recording
│
└── 📁 utils/                     # Utility modules (empty)
```

## Key Files for Developers

### Essential Configuration
- **`.env.example`** - Copy this to `.env` and adjust settings
- **`docker-compose.yml`** - Main Docker configuration
- **`backend/requirements.txt`** - Python dependencies
- **`frontend/package.json`** - Node dependencies

### Core Application Logic
- **`backend/main.py`** - WebSocket server & API endpoints
- **`backend/whisper_service.py`** - GPU/CPU model management
- **`backend/audio_processor.py`** - Handles PCM & WebM audio
- **`frontend/src/hooks/useAudioRecorderPCM.js`** - Real-time audio capture

### Docker Builds
- **`backend/Dockerfile`** - GPU-enabled Python container
- **`frontend/Dockerfile`** - Nginx production server
- **`docker-compose.yml`** - Orchestrates both services

### Launcher Scripts
- **`scripts/run_app.sh`** - Launches web application (frontend + backend)
- **`scripts/gpu_launcher.sh`** - Runs CLI with proper CUDA setup
- **`scripts/run.py`** - Python entry point for CLI

## Development Notes

- Frontend runs on port **6542** (configurable)
- Backend runs on port **6541** (configurable)
- WebSocket endpoint: `ws://localhost:6541/ws`
- Models are cached in Docker volume `whisper-models`
- Audio streams as raw PCM float32 @ 16kHz
- GPU acceleration via NVIDIA Docker runtime

## Clean Root Directory

The root directory now contains only essential files:
- Main documentation (README, QUICKSTART, TROUBLESHOOTING)
- Docker configuration files
- Environment configuration (.env files)
- Git configuration (.gitignore)

All other files have been organized into appropriate subdirectories for better maintainability.