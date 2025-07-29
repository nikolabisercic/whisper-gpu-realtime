#!/bin/bash
# Start the FastAPI server with proper CUDA configuration

echo "🚀 Starting Speech-to-Text Server..."

# Get the directory of this script
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"

# Find CUDA libraries from virtual environment
VENV_PATH="/home/nikola/envs/text2speach"
if [ -d "$VENV_PATH" ]; then
    CT2_LIBS="$VENV_PATH/lib/python3.12/site-packages/ctranslate2.libs"
    CUDNN_PATH="$VENV_PATH/lib/python3.12/site-packages/nvidia/cudnn/lib"
    CUBLAS_PATH="$VENV_PATH/lib/python3.12/site-packages/nvidia/cublas/lib"
    
    export LD_LIBRARY_PATH="${CT2_LIBS}:${CUDNN_PATH}:${CUBLAS_PATH}:${LD_LIBRARY_PATH}"
    echo "✓ CUDA libraries configured"
fi

# Additional environment variables
export CUDA_MODULE_LOADING=LAZY
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Start the server
cd "$BACKEND_DIR"
exec uvicorn main:app --host 0.0.0.0 --port 6541 --reload