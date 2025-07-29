#!/bin/bash

# Set NVIDIA library paths
export LD_LIBRARY_PATH=$(python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'):$LD_LIBRARY_PATH

# Run speech-to-text
python speech_to_text.py "$@"