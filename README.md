# 🎤 GPU-Accelerated Speech-to-Text with Whisper

Real-time speech-to-text using OpenAI Whisper with **NVIDIA GPU acceleration**. Features a clean web interface with live transcription as you speak!

## 🚀 Quick Start (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/text2speach.git
cd text2speach

# 2. Copy environment template
cp .env.example .env

# 3. Build and run with Docker
docker compose up --build

# 4. Open in browser
http://localhost:6542
```

**That's it!** First run downloads models (~2 minutes), then you're ready to transcribe.

> **Note**: Make sure you have [NVIDIA Docker runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) installed for GPU support.

## ✨ What You Get

- **Real-time transcription** - See text appear as you speak (200ms latency)
- **GPU acceleration** - 4-6x faster than CPU with NVIDIA GPUs
- **Beautiful UI** - Clean, modern interface built with React
- **Zero configuration** - Works out of the box with Docker
- **Raw PCM streaming** - Reliable audio capture without codec issues

## 🚀 Alternative: Run Without Docker

If you prefer to run without Docker:

```bash
# 1. Activate virtual environment
source ~/envs/text2speach/bin/activate

# 2. Run both services
./scripts/run_app.sh

# 3. Open in browser
http://localhost:6542
```

## 🎯 Features

- **🎙️ Real-time transcription** from microphone (not file upload)
- **⚡ GPU acceleration** with RTX 4060 (4-6x faster than CPU)
- **🎨 Clean web interface** with React and Tailwind CSS
- **🔄 Model hot-swapping** without restart
- **📋 One-click copy** of transcribed text
- **⌨️ Keyboard shortcuts** (spacebar to record)
- **🐳 Docker deployment** for easy setup

## 📊 System Requirements

### Minimum Requirements

- **GPU**: NVIDIA GPU with 4GB+ VRAM (GTX 1060 or newer)
- **RAM**: 8GB system memory
- **Microphone**: Any standard microphone
- **OS**: Linux, macOS, or Windows with WSL2

### Recommended Setup

- **GPU**: RTX 2060 or better (6GB+ VRAM)
- **RAM**: 16GB for smooth performance
- **Network**: Low-latency for best real-time experience

### Software Prerequisites

- **Docker** & **Docker Compose** v2+
- **NVIDIA Docker runtime** (for GPU support)
- **Modern browser** (Chrome, Firefox, Safari, Edge)

## 🏗️ Architecture

```
text2speach/
├── frontend/               # React + Tailwind CSS
│   ├── src/               # React components & hooks
│   ├── Dockerfile         # Production build
│   └── nginx.conf         # Nginx configuration
├── backend/               # FastAPI + WebSocket
│   ├── main.py           # API server
│   ├── whisper_service.py # Whisper integration
│   ├── audio_processor.py # PCM/WebM processing
│   └── Dockerfile        # GPU-enabled container
├── docker-compose.yml     # Orchestration
└── .env.example          # Configuration template
```

See [REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md) for complete file listing.

## 🔧 Configuration

### Ports

- Frontend: `6542`
- Backend: `6541`

### Environment Variables

A `.env` file has been created with default settings. You can modify these values:

```bash
# Docker Compose Build Optimization (speeds up builds)
COMPOSE_BAKE=true

# GPU Configuration (0 for first GPU)
CUDA_VISIBLE_DEVICES=0

# Default Whisper Model (tiny/base/small/medium)
DEFAULT_MODEL=small

# Development Mode
DEVELOPMENT=false

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:6542

# Backend URL (for frontend to connect)
VITE_BACKEND_URL=http://localhost:6541
```

## 🐳 Docker Commands

### Production

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Remove volumes (models cache)
docker compose down -v
```

### Development

```bash
# Run with hot-reloading
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Rebuild after changes
docker compose build --no-cache
```

## 📊 Model Performance

| Model      | Speed      | Accuracy   | VRAM  | Docker Load Time |
| ---------- | ---------- | ---------- | ----- | ---------------- |
| **tiny**   | ⚡⚡⚡⚡⚡ | ⭐⭐       | 1GB   | ~10s             |
| **base**   | ⚡⚡⚡⚡   | ⭐⭐⭐     | 1.5GB | ~15s             |
| **small**  | ⚡⚡⚡     | ⭐⭐⭐⭐   | 2.5GB | ~20s             |
| **medium** | ⚡⚡       | ⭐⭐⭐⭐⭐ | 5GB   | ~30s             |

## 🔍 Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**

```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**"NVIDIA runtime not found"**

```bash
# Install NVIDIA Docker runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**"GPU not available in container"**

```bash
# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Application Issues

**"WebSocket connection failed"**

- Check if backend is running: `docker compose ps`
- Check backend logs: `docker compose logs backend`

**"Microphone not working"**

- Browser permissions: Allow microphone access
- Test microphone: `docker compose exec backend python tests/test_microphone.py`

**"Model loading slow"**

- First run downloads models (~1-2GB)
- Models are cached in Docker volume for faster subsequent starts

## 📦 Building for Production

### 1. Build optimized images

```bash
docker compose build --no-cache
```

### 2. Tag images

```bash
docker tag text2speach_backend:latest your-registry/speech-backend:v1.0
docker tag text2speach_frontend:latest your-registry/speech-frontend:v1.0
```

### 3. Push to registry

```bash
docker push your-registry/speech-backend:v1.0
docker push your-registry/speech-frontend:v1.0
```

## 🔒 Security Considerations

- The default setup allows all CORS origins (`*`) - restrict in production
- No authentication implemented - add for public deployment
- Models are cached locally - ensure adequate disk space
- GPU access requires privileged container mode

## 🚀 Deployment Options

### Local Machine

Use the provided `docker-compose.yml`

### Cloud with GPU (AWS/GCP/Azure)

1. Use GPU-enabled instances (e.g., AWS g4dn.xlarge)
2. Install NVIDIA drivers and Docker runtime
3. Deploy with docker compose

### Kubernetes

Convert docker-compose to K8s manifests using Kompose:

```bash
kompose convert
```

## 📈 Performance Optimization

- **Model Selection**: Use smaller models for better latency
- **Batch Processing**: Adjust chunk duration in `audio_processor.py`
- **GPU Memory**: Monitor with `nvidia-smi` inside container
- **Caching**: Models are cached in Docker volume

## 🛠️ Development

### Adding New Features

1. Frontend: Edit files in `frontend/src/`
2. Backend: Edit files in `backend/`
3. Rebuild: `docker compose build`

### Running Tests

```bash
# Backend tests
docker compose exec backend pytest

# Frontend tests
docker compose exec frontend npm test
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 2 minutes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues & fixes
- **[REPOSITORY_STRUCTURE.md](docs/REPOSITORY_STRUCTURE.md)** - Project file guide
- **[WEB_APP_README.md](docs/WEB_APP_README.md)** - Web interface details

## 🤝 For Developers

1. **Fork & Clone**:

   ```bash
   git clone https://github.com/yourusername/text2speach.git
   cd text2speach
   cp .env.example .env
   ```

2. **Configure** (optional):

   - Edit `.env` for custom ports or GPU selection
   - Choose model size (tiny/base/small/medium)

3. **Run**:

   ```bash
   docker compose up --build
   ```

4. **Develop**:
   - Frontend hot reload: Edit files in `frontend/src/`
   - Backend changes: Restart with `docker compose restart backend`
   - See [Development Guide](docs/DEVELOPMENT.md) for more

## 📝 License

This project uses:

- faster-whisper (MIT License)
- OpenAI Whisper models (MIT License)
- React (MIT License)
- FastAPI (MIT License)

---

Built with ❤️ using Docker, faster-whisper, and NVIDIA CUDA
