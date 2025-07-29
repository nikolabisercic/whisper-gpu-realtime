#!/bin/bash

# Wrapper script to run speech-to-text with proper environment

# Get CUDA library paths from Python
CUDA_LIBS=$(python3 -c "
import os
try:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    print(f'{os.path.dirname(nvidia.cudnn.lib.__file__)}:{os.path.dirname(nvidia.cublas.lib.__file__)}')
except:
    print('')
" 2>/dev/null)

if [ -n "$CUDA_LIBS" ]; then
    export LD_LIBRARY_PATH="$CUDA_LIBS:$LD_LIBRARY_PATH"
    echo "✓ CUDA libraries configured: $CUDA_LIBS"
else
    echo "⚠ Could not find CUDA libraries"
fi

# Additional environment variables
export CT2_USE_EXPERIMENTAL_CUDNN_V8=1
export CUDA_MODULE_LOADING=LAZY

# Run the script
exec python3 stt_fixed.py "$@"