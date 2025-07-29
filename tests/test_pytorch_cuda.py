#!/usr/bin/env python3
"""Test PyTorch CUDA installation"""

import torch

def test_pytorch_cuda():
    print("=== PyTorch CUDA Test ===")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"Number of GPUs: {torch.cuda.device_count()}")
        print(f"Current GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        # Simple GPU test
        x = torch.rand(5, 3).cuda()
        print(f"\n✓ Successfully created tensor on GPU: {x.device}")
        return True
    else:
        print("✗ CUDA not available")
        return False

if __name__ == "__main__":
    success = test_pytorch_cuda()
    if success:
        print("\n✓ PyTorch with CUDA is working correctly!")
    else:
        print("\n✗ PyTorch CUDA setup failed")