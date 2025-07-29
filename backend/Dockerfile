FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install NVIDIA libraries for faster-whisper
RUN pip3 install --no-cache-dir nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*

# Copy backend code
COPY backend/ ./backend/
COPY src/ ./src/
COPY scripts/ ./scripts/

# Set environment variables for CUDA
ENV CUDA_MODULE_LOADING=LAZY
ENV CT2_USE_EXPERIMENTAL_CUDNN_V8=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH

# Create directory for model cache
RUN mkdir -p /root/.cache/huggingface

# Expose port
EXPOSE 6541

# Run the application
CMD ["python3", "backend/main.py"]