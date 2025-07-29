# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🎤 Audio/Microphone Issues

#### "Microphone access denied"

- **Browser Permission**: Click the lock icon in address bar → Site Settings → Microphone → Allow
- **System Permission**: Check system settings for microphone permissions
- **Try Different Browser**: Chrome and Firefox have best WebRTC support

#### "No audio being captured"

1. Check browser console (F12) for errors
2. Verify microphone is working: `arecord -l` (Linux) or Sound Settings
3. Try a different microphone or USB port
4. Restart browser and Docker containers

#### "Transcription not appearing"

- Check Docker logs: `docker compose logs -f backend`
- Ensure you're speaking clearly and loud enough
- Try a different model (tiny for testing): Change in UI dropdown

### 🖥️ GPU Issues

#### "GPU not detected" or falling back to CPU

```bash
# 1. Check NVIDIA drivers
nvidia-smi

# 2. Test Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi

# 3. Install NVIDIA Docker runtime if missing
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

#### "CUDA out of memory"

- Use a smaller model (tiny or base)
- Close other GPU applications
- Check GPU memory: `nvidia-smi`
- Restart containers: `docker compose restart`

### 🐳 Docker Issues

#### "Cannot connect to Docker daemon"

```bash
# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### "Port already in use"

```bash
# Check what's using the port
sudo lsof -i :6542
sudo lsof -i :6541

# Change ports in .env file
FRONTEND_PORT=6543
BACKEND_PORT=6544
```

#### "Build takes forever"

- First build downloads large images (2-3GB)
- Subsequent builds use cache
- Ensure stable internet connection
- Use `COMPOSE_BAKE=true` in .env for faster builds

### 🌐 WebSocket Issues

#### "WebSocket connection failed"

1. Check backend is running: `docker compose ps`
2. Check backend logs: `docker compose logs backend`
3. Verify firewall isn't blocking ports 6541/6542
4. Try accessing backend directly: <http://localhost:6541/health>

#### "Connection keeps dropping"

- Check network stability
- Increase WebSocket timeout in backend
- Check for proxy/firewall interference

### 🏗️ Build Errors

#### "Package not found" during build

```bash
# Clean rebuild
docker compose down
docker system prune -f
docker compose build --no-cache
```

#### "Permission denied" errors

```bash
# Fix Docker permissions
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### 🎯 Performance Issues

#### "Transcription is slow"

- Switch to GPU (check GPU detection above)
- Use smaller model (tiny/base)
- Check CPU/GPU usage: `htop` and `nvidia-smi`
- Ensure no other heavy processes running

#### "High latency"

- PCM streaming should have ~200ms latency
- Check network if running remotely
- Verify browser supports Web Audio API
- Try closing other browser tabs

### 🔍 Debugging Steps

1. **Check all logs**:

   ```bash
   docker compose logs -f
   ```

2. **Test backend health**:

   ```bash
   curl http://localhost:6541/health
   ```

3. **Check GPU inside container**:

   ```bash
   docker compose exec backend nvidia-smi
   ```

4. **Test microphone in container**:

   ```bash
   docker compose exec backend python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

### 💡 Still Having Issues?

1. **Collect debug info**:

   ```bash
   docker compose logs > debug.log
   nvidia-smi >> debug.log
   docker version >> debug.log
   ```

2. **Open an issue** with:
   - Your system specs (GPU, OS, Docker version)
   - The debug.log file
   - Steps to reproduce the issue
   - What you've already tried

### 🚀 Pro Tips

- **Development mode**: Set `DEVELOPMENT=true` in .env for more verbose logging
- **Model testing**: Start with 'tiny' model to verify everything works
- **Browser console**: F12 → Console tab shows frontend errors
- **Docker stats**: `docker stats` shows resource usage in real-time

---

Remember: Most issues are related to GPU setup or microphone permissions. The application is designed to work out-of-the-box with proper Docker and NVIDIA setup!
