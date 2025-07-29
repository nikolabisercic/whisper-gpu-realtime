#!/usr/bin/env python3
"""Test faster-whisper basic functionality"""

import os
import sys

# Setup environment
os.environ['CT2_USE_EXPERIMENTAL_CUDNN_V8'] = '1'
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'

try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    cublas_dir = os.path.dirname(nvidia.cublas.lib.__file__)
    cudnn_dir = os.path.dirname(nvidia.cudnn.lib.__file__)
    os.environ['LD_LIBRARY_PATH'] = f"{cudnn_dir}:{cublas_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"
    print(f"✓ Set LD_LIBRARY_PATH")
except:
    print("⚠ Could not set CUDA paths")

print("\nTesting faster-whisper import...")
try:
    from faster_whisper import WhisperModel
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

print("\nTesting model load (CPU)...")
try:
    model = WhisperModel("tiny", device="cpu", compute_type="float32")
    print("✓ CPU model loaded")
    del model
except Exception as e:
    print(f"✗ CPU model failed: {e}")

print("\nTesting transcription on test file...")
try:
    model = WhisperModel("tiny", device="cpu", compute_type="float32")
    if os.path.exists("test_recording.wav"):
        segments, info = model.transcribe("test_recording.wav")
        text = " ".join(segment.text for segment in segments)
        print(f"✓ Transcription: {text[:100]}...")
    else:
        print("⚠ No test_recording.wav found")
    del model
except Exception as e:
    print(f"✗ Transcription failed: {e}")

print("\nTesting CUDA model load...")
try:
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("✓ CUDA model loaded")
    del model
except Exception as e:
    print(f"✗ CUDA model failed: {e}")
    print("\nTrying with int8...")
    try:
        model = WhisperModel("tiny", device="cuda", compute_type="int8_float16")
        print("✓ CUDA int8 model loaded")
        del model
    except Exception as e2:
        print(f"✗ CUDA int8 also failed: {e2}")

print("\nTest complete.")