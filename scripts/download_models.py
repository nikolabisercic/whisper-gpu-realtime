#!/usr/bin/env python3
"""Download Whisper models for faster-whisper"""

import os
import sys

# Set NVIDIA library paths before importing
try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    cublas_dir = os.path.dirname(nvidia.cublas.lib.__file__)
    cudnn_dir = os.path.dirname(nvidia.cudnn.lib.__file__) 
    os.environ['LD_LIBRARY_PATH'] = f"{cublas_dir}:{cudnn_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"
except ImportError:
    pass

from faster_whisper import WhisperModel
import argparse

def download_model(model_name):
    """Download a specific Whisper model"""
    print(f"\n{'='*50}")
    print(f"Downloading Whisper model: {model_name}")
    print('='*50)
    
    try:
        # Initialize model (this triggers download if not cached)
        print(f"Initializing {model_name} model...")
        model = WhisperModel(model_name, device="cpu")  # Use CPU for download only
        print(f"✓ Model {model_name} downloaded and cached successfully")
        
        # Clean up
        del model
        
    except Exception as e:
        print(f"✗ Error downloading {model_name}: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Download Whisper models")
    parser.add_argument("--models", nargs="+", 
                       default=["tiny", "base", "small", "medium"],
                       choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
                       help="Models to download")
    
    args = parser.parse_args()
    
    print("Whisper Model Downloader")
    print("="*50)
    print(f"Models to download: {', '.join(args.models)}")
    
    success = []
    failed = []
    
    for model in args.models:
        if download_model(model):
            success.append(model)
        else:
            failed.append(model)
    
    print("\n" + "="*50)
    print("Download Summary:")
    print(f"✓ Successfully downloaded: {', '.join(success) if success else 'None'}")
    if failed:
        print(f"✗ Failed to download: {', '.join(failed)}")
    
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())