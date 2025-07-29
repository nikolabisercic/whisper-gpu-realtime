#!/usr/bin/env python3
"""Test microphone access and audio recording"""

import sounddevice as sd
import numpy as np
import wave
import sys

def list_audio_devices():
    """List all available audio devices"""
    print("=== Available Audio Devices ===")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")
        print(f"   Input channels: {device['max_input_channels']}, Output channels: {device['max_output_channels']}")
        print(f"   Host API: {sd.query_hostapis(device['hostapi'])['name']}")
        if device['max_input_channels'] > 0:
            print("   ✓ Input device (microphone)")
        if device['max_output_channels'] > 0:
            print("   ✓ Output device (speaker)")
    
    default_input = sd.query_devices(kind='input')
    print(f"\nDefault input device: {default_input['name']}")
    return default_input

def test_recording(duration=3):
    """Test recording from microphone"""
    sample_rate = 16000  # Whisper uses 16kHz
    channels = 1
    
    print(f"\n=== Recording Test ===")
    print(f"Recording for {duration} seconds...")
    print("Speak now!")
    
    try:
        # Record audio
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=channels,
                          dtype=np.float32)
        sd.wait()  # Wait for recording to complete
        
        print("✓ Recording completed")
        
        # Check if we got audio
        max_amplitude = np.max(np.abs(recording))
        print(f"Max amplitude: {max_amplitude:.4f}")
        
        if max_amplitude > 0.001:
            print("✓ Audio detected")
            
            # Save to file
            filename = "test_recording.wav"
            recording_int16 = (recording * 32767).astype(np.int16)
            
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(recording_int16.tobytes())
            
            print(f"✓ Saved to {filename}")
            return True
        else:
            print("⚠ No audio detected - check microphone")
            return False
            
    except Exception as e:
        print(f"✗ Error recording: {e}")
        return False

def main():
    """Main test function"""
    print("Microphone Test Script")
    print("=" * 50)
    
    # List devices
    default_device = list_audio_devices()
    
    # Test recording
    success = test_recording(3)
    
    if success:
        print("\n✓ Microphone is working correctly!")
        print("✓ Ready for speech-to-text setup")
    else:
        print("\n✗ Microphone test failed")
        print("Please check your microphone settings")

if __name__ == "__main__":
    main()