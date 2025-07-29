"""Audio processing utilities for WebSocket streaming"""

import io
import numpy as np
import logging
from pydub import AudioSegment
import asyncio
import base64

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Process audio data from WebSocket"""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.audio_buffer = []
        self.chunk_duration_ms = 5000  # 5 seconds chunks
        
    async def process_audio_chunk(self, audio_data: bytes, format: str = "webm") -> np.ndarray:
        """Convert audio chunk to numpy array for Whisper"""
        try:
            # If data is base64 encoded
            if isinstance(audio_data, str):
                # Remove data URL prefix if present
                if audio_data.startswith('data:audio'):
                    audio_data = audio_data.split(',')[1]
                audio_data = base64.b64decode(audio_data)
            
            # Handle PCM format (raw float32 data)
            if format == "pcm":
                # Convert bytes directly to float32 numpy array
                # The data is already normalized [-1, 1] from the frontend
                samples = np.frombuffer(audio_data, dtype=np.float32)
                return samples
            
            # Handle other formats (webm, etc.) using pydub
            audio = AudioSegment.from_file(
                io.BytesIO(audio_data), 
                format=format
            )
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Resample to target sample rate
            audio = audio.set_frame_rate(self.sample_rate)
            
            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples())
            
            # Normalize to float32 [-1, 1]
            if audio.sample_width == 2:  # 16-bit
                samples = samples.astype(np.float32) / 32768.0
            elif audio.sample_width == 4:  # 32-bit
                samples = samples.astype(np.float32) / 2147483648.0
            else:
                samples = samples.astype(np.float32)
            
            return samples
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            raise
    
    def add_to_buffer(self, audio_array: np.ndarray):
        """Add audio to buffer"""
        self.audio_buffer.extend(audio_array.tolist())
    
    def get_buffer_duration_ms(self) -> float:
        """Get current buffer duration in milliseconds"""
        return (len(self.audio_buffer) / self.sample_rate) * 1000
    
    def should_process_buffer(self) -> bool:
        """Check if buffer has enough audio to process"""
        return self.get_buffer_duration_ms() >= self.chunk_duration_ms
    
    def get_and_clear_buffer(self) -> np.ndarray:
        """Get buffer contents and clear it"""
        audio_data = np.array(self.audio_buffer, dtype=np.float32)
        self.audio_buffer = []
        return audio_data
    
    def clear_buffer(self):
        """Clear the audio buffer"""
        self.audio_buffer = []