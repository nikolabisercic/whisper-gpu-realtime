#!/usr/bin/env python3
"""Robust GPU launcher for speech-to-text"""

import os
import sys
import subprocess

def find_cuda_libraries():
    """Find and return CUDA library paths"""
    paths = []
    
    # Try to find via pip packages
    try:
        import nvidia.cublas.lib
        import nvidia.cudnn.lib
        paths.append(os.path.dirname(nvidia.cudnn.lib.__file__))
        paths.append(os.path.dirname(nvidia.cublas.lib.__file__))
        print(f"✓ Found CUDA libraries via pip packages")
    except ImportError:
        pass
    
    # Try common locations
    common_paths = [
        "/usr/local/cuda/lib64",
        "/usr/lib/x86_64-linux-gnu",
        "/opt/cuda/lib64",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            paths.append(path)
    
    return ":".join(paths)

def main():
    """Launch speech-to-text with proper environment"""
    
    print("🚀 GPU Speech-to-Text Launcher")
    print("="*40)
    
    # Get library paths
    lib_paths = find_cuda_libraries()
    
    # Setup environment
    env = os.environ.copy()
    
    # Set library paths
    current_ld = env.get('LD_LIBRARY_PATH', '')
    if lib_paths:
        env['LD_LIBRARY_PATH'] = f"{lib_paths}:{current_ld}" if current_ld else lib_paths
        print(f"✓ Library paths configured")
    
    # Set additional CUDA environment variables
    env['CUDA_MODULE_LOADING'] = 'LAZY'
    env['CT2_USE_EXPERIMENTAL_CUDNN_V8'] = '1'
    env['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU
    
    # Disable some warnings
    env['TF_CPP_MIN_LOG_LEVEL'] = '2'
    env['PYTHONWARNINGS'] = 'ignore'
    
    # Get the main script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    main_script = os.path.join(project_root, "src", "speech_to_text.py")
    
    # Build command
    cmd = [sys.executable, main_script] + sys.argv[1:]
    
    print(f"✓ Starting with GPU acceleration...\n")
    
    try:
        # Run the main script with the configured environment
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n✓ Stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()