#!/usr/bin/env python3
"""Real-time speech-to-text using faster-whisper with GPU acceleration"""

import os
import sys

# CRITICAL: Set CUDA library paths BEFORE any imports that use CUDA
def setup_cuda_paths():
    """Setup CUDA library paths before imports"""
    try:
        # Import nvidia libraries to get paths
        import nvidia.cublas.lib
        import nvidia.cudnn.lib
        
        cublas_path = os.path.dirname(nvidia.cublas.lib.__file__)
        cudnn_path = os.path.dirname(nvidia.cudnn.lib.__file__)
        
        # Get current LD_LIBRARY_PATH
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        
        # Prepend CUDA paths
        new_ld_path = f"{cudnn_path}:{cublas_path}"
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        
        # Also set for ctranslate2
        os.environ['CT2_USE_EXPERIMENTAL_CUDNN_V8'] = '1'
        os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
        
        # Force reload of dynamic libraries
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(cudnn_path)
            os.add_dll_directory(cublas_path)
            
        return True
    except ImportError:
        return False

# Setup CUDA before any other imports
cuda_available = setup_cuda_paths()

# Now safe to import everything else
import sounddevice as sd
import numpy as np
import queue
import threading
import time
import argparse
import signal
from faster_whisper import WhisperModel
import warnings
warnings.filterwarnings("ignore")

class SpeechToText:
    def __init__(self, model_size="tiny", device="cuda", compute_type="float16"):
        # Check if CUDA is actually available when requested
        actual_device = device
        if device == "cuda":
            try:
                # Test CUDA availability
                import torch
                if not torch.cuda.is_available():
                    print("\n⚠️  WARNING: CUDA requested but not available!")
                    print("⚠️  FALLING BACK TO CPU (slower performance)")
                    print("⚠️  This may take longer to process audio\n")
                    actual_device = "cpu"
            except:
                print("\n⚠️  WARNING: CUDA requested but PyTorch not properly configured!")
                print("⚠️  FALLING BACK TO CPU (slower performance)\n")
                actual_device = "cpu"
        
        if actual_device == "cpu" and device == "cuda":
            print("💡 TIP: Check CUDA installation or use --device cpu to hide this warning\n")
        
        print(f"Loading {model_size} model on {actual_device.upper()}...")
        compute_type = "float16" if actual_device == "cuda" else "float32"
        
        try:
            self.model = WhisperModel(model_size, device=actual_device, compute_type=compute_type)
            if actual_device == "cuda":
                print("✓ Model loaded on GPU (fast transcription)")
            else:
                print("✓ Model loaded on CPU (may be slower)")
        except Exception as e:
            if "cuda" in str(e).lower() and actual_device == "cuda":
                print("\n⚠️  CUDA ERROR: Failed to load on GPU, retrying with CPU...")
                self.model = WhisperModel(model_size, device="cpu", compute_type="float32")
                print("✓ Model loaded on CPU (fallback mode)")
            else:
                raise e
        
        print("✓ Ready to transcribe!")
        
        self.sample_rate = 16000
        self.recording = False
        self.audio_queue = queue.Queue()
        
    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())
    
    def transcribe_stream(self):
        """Process audio in chunks"""
        buffer = []
        chunk_length = int(self.sample_rate * 5)  # 5 second chunks
        
        print("\nListening... Speak now! (Ctrl+C to stop)\n")
        
        with sd.InputStream(samplerate=self.sample_rate, channels=1, 
                          callback=self.callback, dtype=np.float32):
            while True:
                try:
                    # Get audio data
                    data = self.audio_queue.get(timeout=0.5)
                    buffer.extend(data.flatten())
                    
                    # Process chunk when ready
                    if len(buffer) >= chunk_length:
                        audio = np.array(buffer[:chunk_length])
                        buffer = buffer[chunk_length:]
                        
                        # Skip silence
                        if np.max(np.abs(audio)) > 0.01:
                            # Transcribe
                            segments, _ = self.model.transcribe(audio, beam_size=5, language="en")
                            text = " ".join(s.text for s in segments).strip()
                            
                            if text:
                                print(f"→ {text}")
                                
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    print("\n\nStopping...")
                    break

def main():
    parser = argparse.ArgumentParser(description="Real-time speech-to-text")
    parser.add_argument("--model", default="tiny", 
                       choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
                       help="Model size (tiny=fastest, medium=best quality)")
    parser.add_argument("--device", default="cuda",
                       choices=["cuda", "cpu"], 
                       help="Processing device")
    parser.add_argument("--compute-type", default="float16",
                       choices=["float16", "int8_float16", "float32"],
                       help="Computation type")
    
    args = parser.parse_args()
    
    # Print CUDA setup status
    if cuda_available:
        print("✓ CUDA libraries configured")
    else:
        print("⚠ CUDA libraries not found, will use CPU if CUDA fails")
    
    # Create STT instance
    stt = SpeechToText(model_size=args.model, device=args.device, compute_type=args.compute_type)
    
    # Start transcribing
    try:
        stt.transcribe_stream()
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()