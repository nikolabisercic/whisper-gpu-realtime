"""FastAPI server for Speech-to-Text with WebSocket support"""

import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import logging
import asyncio
from typing import Dict, Any

from contextlib import asynccontextmanager
from whisper_service import whisper_service
from audio_processor import AudioProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Connection manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Speech-to-Text server...")
    # Load default model
    success = await whisper_service.load_model("small")
    if success:
        logger.info("✓ Server ready")
    else:
        logger.error("Failed to load initial model")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Speech-to-Text server...")

# Create FastAPI app with lifespan
app = FastAPI(title="Speech-to-Text API", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6542", "http://localhost:5173", "*"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Speech-to-Text API",
        "endpoints": {
            "websocket": "/ws",
            "models": "/models",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": whisper_service.model is not None,
        "device": whisper_service.device
    }

@app.get("/models")
async def get_models():
    """Get available models and current status"""
    return whisper_service.get_model_info()

@app.post("/models/{model_name}")
async def change_model(model_name: str):
    """Change the active model"""
    if model_name not in whisper_service.models_info:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid model: {model_name}"}
        )
    
    success = await whisper_service.load_model(model_name)
    if success:
        return {"message": f"Model changed to {model_name}", "device": whisper_service.device}
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to load model"}
        )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for audio streaming"""
    await manager.connect(websocket)
    audio_processor = AudioProcessor()
    
    try:
        # Send initial connection message
        await manager.send_json(websocket, {
            "type": "connection",
            "status": "connected",
            "model": whisper_service.current_model_size,
            "device": whisper_service.device
        })
        
        while True:
            # Receive message from client
            message = await websocket.receive_json()
            
            if message["type"] == "audio":
                # Process audio data
                try:
                    audio_data = message["data"]
                    format = message.get("format", "webm")
                    
                    # Convert audio chunk
                    audio_array = await audio_processor.process_audio_chunk(audio_data, format)
                    audio_processor.add_to_buffer(audio_array)
                    
                    # Check if we have enough audio to process
                    if audio_processor.should_process_buffer():
                        audio_to_process = audio_processor.get_and_clear_buffer()
                        
                        # Send processing status
                        await manager.send_json(websocket, {
                            "type": "status",
                            "message": "Processing audio..."
                        })
                        
                        # Transcribe audio
                        async for result in whisper_service.transcribe_audio(audio_to_process):
                            await manager.send_json(websocket, result)
                    
                except Exception as e:
                    logger.error(f"Audio processing error: {e}")
                    await manager.send_json(websocket, {
                        "type": "error",
                        "message": f"Audio processing error: {str(e)}"
                    })
            
            elif message["type"] == "change_model":
                # Change model
                model_name = message["model"]
                await manager.send_json(websocket, {
                    "type": "status",
                    "message": f"Loading {model_name} model..."
                })
                
                success = await whisper_service.load_model(model_name)
                if success:
                    await manager.send_json(websocket, {
                        "type": "model_changed",
                        "model": model_name,
                        "device": whisper_service.device
                    })
                else:
                    await manager.send_json(websocket, {
                        "type": "error",
                        "message": "Failed to load model"
                    })
            
            elif message["type"] == "ping":
                # Respond to ping
                await manager.send_json(websocket, {"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6541)