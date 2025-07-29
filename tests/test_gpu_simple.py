#!/usr/bin/env python3
"""Simple GPU test without subprocess issues"""

import os
import sys

# Set paths before imports
try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    os.environ['LD_LIBRARY_PATH'] = f"{os.path.dirname(nvidia.cudnn.lib.__file__)}:{os.path.dirname(nvidia.cublas.lib.__file__)}:{os.environ.get('LD_LIBRARY_PATH', '')}"
    print("✓ CUDA paths set")
except:
    print("⚠ Could not set CUDA paths")

# Test imports
try:
    from faster_whisper import WhisperModel
    print("✓ faster_whisper imported")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test model loading
print("\nTesting GPU model loading...")
try:
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("✅ SUCCESS: GPU model loaded!")
    print("✅ GPU acceleration is working!")
    
    # Quick test
    print("\nTesting transcription...")
    import numpy as np
    test_audio = np.zeros(16000, dtype=np.float32)  # 1 second of silence
    segments, _ = model.transcribe(test_audio)
    print("✅ Transcription test passed!")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nTrying CPU mode...")
    try:
        model = WhisperModel("tiny", device="cpu", compute_type="float32")
        print("✓ CPU model works")
    except Exception as e2:
        print(f"✗ CPU also failed: {e2}")

print("\nDone!")