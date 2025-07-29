#!/usr/bin/env python3
"""Test NVIDIA GPU availability without installing system packages"""

import subprocess
import sys

def test_nvidia_driver():
    """Test if NVIDIA driver is accessible"""
    print("=== Testing NVIDIA Driver Access ===")
    
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ NVIDIA driver is accessible")
            print(f"  Driver info: {result.stdout.split('Driver Version:')[1].split()[0]}")
            print(f"  CUDA Version: {result.stdout.split('CUDA Version:')[1].split()[0]}")
            return True
        else:
            print("✗ NVIDIA driver not accessible")
            return False
    except FileNotFoundError:
        print("✗ nvidia-smi command not found")
        return False
    except Exception as e:
        print(f"✗ Error checking NVIDIA driver: {e}")
        return False

def test_cuda_python():
    """Test if we can import CUDA-related Python packages"""
    print("\n=== Testing Python CUDA Support ===")
    
    # Test if we can import ctypes and access CUDA
    try:
        import ctypes
        
        # Try to load CUDA runtime library
        cuda_paths = [
            '/usr/local/cuda/lib64/libcudart.so',
            '/usr/lib/x86_64-linux-gnu/libcudart.so',
            'libcudart.so'
        ]
        
        cuda_loaded = False
        for path in cuda_paths:
            try:
                ctypes.CDLL(path)
                print(f"✓ CUDA runtime library found at: {path}")
                cuda_loaded = True
                break
            except:
                continue
                
        if not cuda_loaded:
            print("⚠ CUDA runtime library not found in standard locations")
            
    except Exception as e:
        print(f"✗ Error testing CUDA libraries: {e}")

def main():
    """Run all tests"""
    print("NVIDIA GPU Test Script")
    print("=" * 50)
    
    # Test 1: Check driver
    driver_ok = test_nvidia_driver()
    
    # Test 2: Check Python CUDA access
    test_cuda_python()
    
    print("\n=== Summary ===")
    if driver_ok:
        print("✓ NVIDIA drivers are working properly")
        print("✓ Safe to proceed with PyTorch CUDA installation in venv")
    else:
        print("✗ Issues detected with NVIDIA setup")
        print("⚠ Do not install system-wide NVIDIA packages!")

if __name__ == "__main__":
    main()