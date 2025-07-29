#!/usr/bin/env python3
"""Launcher script that properly sets up environment and runs speech-to-text"""

import os
import subprocess
import sys

def main():
    # Get CUDA library paths
    try:
        import nvidia.cublas.lib
        import nvidia.cudnn.lib
        cublas_dir = os.path.dirname(nvidia.cublas.lib.__file__)
        cudnn_dir = os.path.dirname(nvidia.cudnn.lib.__file__)
        
        # Set environment
        env = os.environ.copy()
        env['LD_LIBRARY_PATH'] = f"{cudnn_dir}:{cublas_dir}:{env.get('LD_LIBRARY_PATH', '')}"
        env['CUDA_MODULE_LOADING'] = 'LAZY'
        
        print("✓ CUDA libraries configured")
        print(f"✓ Using: {cudnn_dir}")
        
    except ImportError:
        print("⚠ Running without CUDA acceleration")
        env = os.environ.copy()
    
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    src_path = os.path.join(project_root, "src", "speech_to_text.py")
    
    # Pass command line arguments
    cmd = [sys.executable, src_path] + sys.argv[1:]
    
    print("\nStarting speech-to-text...\n")
    
    # Run the actual script
    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()