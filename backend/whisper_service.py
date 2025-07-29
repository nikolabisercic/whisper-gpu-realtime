"""Whisper model service for transcription"""

import os
import sys
import asyncio
import numpy as np
from typing import Optional, AsyncGenerator, Tuple
import logging

# Set up CUDA paths before imports
def setup_cuda_paths():
    """Setup CUDA library paths before imports"""
    try:
        # Add parent directory to path to access existing code
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        
        import nvidia.cublas.lib
        import nvidia.cudnn.lib
        
        cublas_path = os.path.dirname(nvidia.cublas.lib.__file__)
        cudnn_path = os.path.dirname(nvidia.cudnn.lib.__file__)
        
        # Use ctranslate2 bundled libraries
        ct2_libs = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "..", "lib", "python3.12", "site-packages", "ctranslate2.libs")
        
        if os.path.exists(ct2_libs):
            os.environ['LD_LIBRARY_PATH'] = f"{ct2_libs}:{cudnn_path}:{cublas_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        else:
            os.environ['LD_LIBRARY_PATH'] = f"{cudnn_path}:{cublas_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        
        os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
        return True
    except ImportError:
        return False

# Setup CUDA before imports
cuda_available = setup_cuda_paths()

from faster_whisper import WhisperModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperService:
    """Service for managing Whisper model and transcription"""
    
    def __init__(self):
        self.model = None
        self.current_model_size = None
        self.device = "cuda" if cuda_available else "cpu"
        self.models_info = {
            "tiny": {"size": "39 MB", "speed": 5, "accuracy": 2},
            "base": {"size": "74 MB", "speed": 4, "accuracy": 3},
            "small": {"size": "244 MB", "speed": 3, "accuracy": 4},
            "medium": {"size": "769 MB", "speed": 2, "accuracy": 5}
        }
    
    async def load_model(self, model_size: str = "small") -> bool:
        """Load or switch Whisper model"""
        if self.current_model_size == model_size and self.model is not None:
            logger.info(f"Model {model_size} already loaded")
            return True
        
        try:
            logger.info(f"Loading {model_size} model on {self.device}")
            
            # Load in separate thread to not block
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                None, 
                lambda: WhisperModel(
                    model_size, 
                    device=self.device, 
                    compute_type="float16" if self.device == "cuda" else "float32"
                )
            )
            
            self.current_model_size = model_size
            logger.info(f"✓ Model {model_size} loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Try CPU fallback
            if self.device == "cuda":
                self.device = "cpu"
                return await self.load_model(model_size)
            return False
    
    async def transcribe_audio(self, audio_data: np.ndarray, language: str = "en") -> AsyncGenerator[dict, None]:
        """Transcribe audio and yield results"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            # Run transcription in executor to not block
            loop = asyncio.get_event_loop()
            segments, info = await loop.run_in_executor(
                None,
                lambda: self.model.transcribe(
                    audio_data,
                    beam_size=5,
                    language=language,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500)
                )
            )
            
            # Yield segments as they come
            for segment in segments:
                yield {
                    "type": "transcription",
                    "text": segment.text.strip(),
                    "start": segment.start,
                    "end": segment.end,
                    "final": True
                }
                
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            yield {
                "type": "error",
                "message": str(e)
            }
    
    def get_model_info(self):
        """Get information about available models"""
        return {
            "available_models": list(self.models_info.keys()),
            "current_model": self.current_model_size,
            "device": self.device,
            "cuda_available": cuda_available,
            "models_info": self.models_info
        }

# Global instance
whisper_service = WhisperService()