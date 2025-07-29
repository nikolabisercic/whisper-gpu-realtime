# 🎤 GPU-Accelerated Speech-to-Text with Whisper

Real-time speech-to-text using OpenAI Whisper with **NVIDIA GPU acceleration** on Ubuntu.

## 🚀 Quickstart (2 minutes)

```bash
# 1. Activate your virtual environment
source ~/envs/text2speach/bin/activate

# 2. Run with GPU acceleration
./gpu_launcher.sh --model small --device cuda

# 3. Speak into your microphone!
# Transcriptions appear as: → your speech here
# Press Ctrl+C to stop
```

## ✨ Features

- **Real-time transcription** from microphone (not file upload)
- **GPU acceleration** with your RTX 4060 (4-6x faster than CPU)
- **Multiple models** from tiny (fastest) to medium (most accurate)
- **Clear GPU/CPU indicators** - know exactly what's running
- **Automatic fallback** to CPU if GPU fails

## 📊 System Status

- ✅ **GPU**: NVIDIA RTX 4060 Laptop (8GB VRAM)
- ✅ **CUDA**: Version 12.4
- ✅ **Models**: tiny, base, small, medium (all downloaded)
- ✅ **Libraries**: faster-whisper 1.0.3, ctranslate2 4.6.0

## 🎯 Model Selection Guide

| Model | Speed | Accuracy | VRAM | Recommended For |
|-------|-------|----------|------|-----------------|
| **tiny** | ⚡⚡⚡⚡⚡ | ⭐⭐ | 1GB | Testing, casual use |
| **base** | ⚡⚡⚡⚡ | ⭐⭐⭐ | 1.5GB | Daily use |
| **small** | ⚡⚡⚡ | ⭐⭐⭐⭐ | 2.5GB | **Best balance** ✨ |
| **medium** | ⚡⚡ | ⭐⭐⭐⭐⭐ | 5GB | High accuracy |

## 🛠️ Installation Complete

All dependencies are installed. No additional setup needed!

## 📁 Project Structure

```
text2speach/
├── gpu_launcher.sh         # 🚀 Main launcher (USE THIS!)
├── src/
│   └── speech_to_text.py   # Core implementation
├── scripts/               
│   ├── launch_gpu.py       # Alternative launcher
│   └── download_models.py  # Model downloader
├── tests/                  # Test scripts
├── recordings/             # Saved audio files
└── README.md              # This file
```

## 🎮 Usage Examples

### Basic Usage (Recommended)
```bash
./gpu_launcher.sh --model small --device cuda
```

### Try Different Models
```bash
# Fastest (for testing)
./gpu_launcher.sh --model tiny --device cuda

# Most accurate
./gpu_launcher.sh --model medium --device cuda
```

### Force CPU Mode
```bash
./gpu_launcher.sh --model tiny --device cpu
```

## 🔧 Troubleshooting

### GPU Not Working?

1. **Use the launcher**: Always use `./gpu_launcher.sh` - it sets up the environment correctly
2. **Check GPU status**: Run `nvidia-smi` to verify GPU is available
3. **Library errors**: The launcher handles this automatically

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Unable to load libcudnn_ops" | Use `./gpu_launcher.sh` instead of `python` directly |
| GPU not detected | Check `nvidia-smi`, restart terminal |
| Slow performance | Ensure using `--device cuda`, not `cpu` |
| No transcription | Speak louder, check microphone with `python tests/test_microphone.py` |

## 🎯 Performance Tips

1. **Use GPU**: Always use `--device cuda` for 4-6x faster transcription
2. **Model choice**: Start with `small` for best speed/accuracy balance
3. **Microphone**: Speak clearly, avoid background noise
4. **Chunk size**: Default 5-second chunks work well

## 🧪 Testing

```bash
# Test microphone
python tests/test_microphone.py

# Test GPU setup
python test_gpu_simple.py
```

## 📝 Notes

- **Real-time**: Processes audio in 5-second chunks
- **Language**: Default is English (change with `language` parameter in code)
- **GPU Memory**: Your RTX 4060 can handle all models except large
- **Fallback**: Automatically uses CPU if GPU fails (with clear warnings)

## 🎉 Success!

You now have GPU-accelerated speech-to-text working! The system transcribes your voice in real-time using your RTX 4060 GPU for maximum performance.

---

*Built with ❤️ using faster-whisper and NVIDIA CUDA*