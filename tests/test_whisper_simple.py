#!/usr/bin/env python3
"""Simple test of Whisper transcription on a file"""

import os
import sys

# Set NVIDIA library paths before importing anything else
try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    cublas_dir = os.path.dirname(nvidia.cublas.lib.__file__)
    cudnn_dir = os.path.dirname(nvidia.cudnn.lib.__file__)
    os.environ['LD_LIBRARY_PATH'] = f"{cublas_dir}:{cudnn_dir}"
    print(f"✓ Set LD_LIBRARY_PATH to: {os.environ['LD_LIBRARY_PATH']}")
except ImportError as e:
    print(f"Warning: Could not set NVIDIA library paths: {e}")

from faster_whisper import WhisperModel

def test_transcription():
    """Test transcription on the recorded file"""
    print("\n=== Testing Whisper Transcription ===")
    
    # Check if test recording exists
    if not os.path.exists("test_recording.wav"):
        print("✗ test_recording.wav not found. Run test_microphone.py first.")
        return
    
    # Load model
    print("Loading Whisper model 'small' with float16...")
    model = WhisperModel("small", device="cuda", compute_type="float16")
    print("✓ Model loaded successfully")
    
    # Transcribe
    print("\nTranscribing test_recording.wav...")
    segments, info = model.transcribe("test_recording.wav", beam_size=5)
    
    print(f"\nDetected language: {info.language} (probability: {info.language_probability:.2f})")
    print("\nTranscription:")
    print("-" * 40)
    
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
    
    print("-" * 40)
    print("✓ Transcription complete")

if __name__ == "__main__":
    test_transcription()