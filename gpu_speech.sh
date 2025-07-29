#!/bin/bash
# GPU Speech-to-Text Launcher

echo "🚀 Starting GPU Speech-to-Text..."

# Find CUDA libraries
CUDNN_PATH=$(python3 -c "import nvidia.cudnn.lib; import os; print(os.path.dirname(nvidia.cudnn.lib.__file__))" 2>/dev/null)
CUBLAS_PATH=$(python3 -c "import nvidia.cublas.lib; import os; print(os.path.dirname(nvidia.cublas.lib.__file__))" 2>/dev/null)

if [ -n "$CUDNN_PATH" ] && [ -n "$CUBLAS_PATH" ]; then
    export LD_LIBRARY_PATH="${CUDNN_PATH}:${CUBLAS_PATH}:${LD_LIBRARY_PATH}"
    echo "✓ CUDA libraries found and configured"
else
    echo "⚠ Warning: Could not find CUDA libraries"
fi

# Additional environment variables
export CUDA_MODULE_LOADING=LAZY
export CT2_USE_EXPERIMENTAL_CUDNN_V8=1

# Run the speech-to-text script
exec python3 src/speech_to_text.py "$@"