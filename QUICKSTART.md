# 🚀 Quick Start Guide - GPU Speech-to-Text

Get real-time speech-to-text running in under 5 minutes!

## Prerequisites

- **NVIDIA GPU** with 4GB+ VRAM (RTX 2060 or better recommended)
- **Docker** and **Docker Compose** installed
- **NVIDIA Docker runtime** configured
- **Microphone** connected to your system

## 1-Minute Setup

```bash
# Clone the repository
git clone https://github.com/nikolabisercic/whisper-gpu-realtime.git
cd whisper-gpu-realtime

# Copy environment template
cp .env.example .env

# Build and run
docker compose up --build
```

🎉 **That's it!** Open <http://localhost:6542> in your browser.

## First Time Usage

1. **Wait for model download** (first run only, ~1-2 minutes)
2. **Allow microphone access** when browser prompts
3. **Click the red button** or press **spacebar** to start recording
4. **Speak clearly** - transcription appears in real-time!

## Quick Troubleshooting

### "GPU not available"

```bash
# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

### "Port already in use"

Edit `.env` to change ports:

```
FRONTEND_PORT=6543
BACKEND_PORT=6544
```

### "No microphone detected"

- Check browser permissions (icon in address bar)
- Try a different browser (Chrome/Firefox work best)

## Model Selection

Edit `.env` to change default model:

```bash
DEFAULT_MODEL=tiny    # Fastest, less accurate
DEFAULT_MODEL=small   # Balanced (default)
DEFAULT_MODEL=medium  # Most accurate, slower
```

## Stop & Cleanup

```bash
# Stop services
docker compose down

# Full cleanup (removes downloaded models)
docker compose down -v
```

## Next Steps

- Check [README.md](README.md) for detailed documentation
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Join discussions in Issues/Discussions

---

**Need help?** Open an issue with your `docker compose logs` output.
