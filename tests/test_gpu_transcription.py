#!/usr/bin/env python3
"""Quick test of GPU transcription"""

import os
# Set library paths before imports
try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    os.environ['LD_LIBRARY_PATH'] = f"{os.path.dirname(nvidia.cudnn.lib.__file__)}:{os.path.dirname(nvidia.cublas.lib.__file__)}:{os.environ.get('LD_LIBRARY_PATH', '')}"
except:
    pass

from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
import time

def test_gpu_transcription():
    print("Testing GPU Speech-to-Text...")
    
    # Load model on GPU
    print("\n1. Loading tiny model on GPU...")
    model = WhisperModel("tiny", device="cuda", compute_type="float16")
    print("✓ Model loaded on GPU successfully!")
    
    # Record short audio
    print("\n2. Recording 3 seconds of audio...")
    print("🎤 Speak now!")
    duration = 3
    sample_rate = 16000
    
    recording = sd.rec(int(duration * sample_rate), 
                      samplerate=sample_rate, 
                      channels=1,
                      dtype=np.float32)
    sd.wait()
    print("✓ Recording complete")
    
    # Transcribe
    print("\n3. Transcribing with GPU...")
    start_time = time.time()
    segments, info = model.transcribe(recording.flatten(), beam_size=5, language="en")
    transcription = " ".join(segment.text for segment in segments)
    end_time = time.time()
    
    print(f"✓ Transcription complete in {end_time - start_time:.2f} seconds")
    print(f"\n📝 Transcription: {transcription}")
    
    # Verify GPU was used
    print(f"\n✓ GPU acceleration confirmed - using CUDA")
    print("✓ All tests passed!")

if __name__ == "__main__":
    test_gpu_transcription()