#!/bin/bash
# GPU Speech-to-Text Launcher with proper library ordering

echo "🚀 GPU Speech-to-Text Launcher"
echo "================================"

# Set the ctranslate2 bundled libraries first
CT2_LIBS="/home/nikola/envs/text2speach/lib/python3.12/site-packages/ctranslate2.libs"

# Then add the NVIDIA libraries
NVIDIA_LIBS="/home/nikola/envs/text2speach/lib/python3.12/site-packages/nvidia/cudnn/lib:/home/nikola/envs/text2speach/lib/python3.12/site-packages/nvidia/cublas/lib"

# Set the library path with ctranslate2 libs first
export LD_LIBRARY_PATH="${CT2_LIBS}:${NVIDIA_LIBS}:${LD_LIBRARY_PATH}"

# Additional environment variables
export CUDA_MODULE_LOADING=LAZY
export OMP_NUM_THREADS=4

echo "✓ Libraries configured"
echo "✓ Using ctranslate2 bundled CUDNN"
echo ""

# Run the speech-to-text
exec python src/speech_to_text.py "$@"