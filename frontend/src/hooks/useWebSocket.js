import { useState, useEffect, useCallback, useRef } from 'react';

const WS_URL = process.env.NODE_ENV === 'production' 
  ? `ws://${window.location.host}/ws`
  : 'ws://localhost:6541/ws';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [device, setDevice] = useState('cpu');
  const [currentModel, setCurrentModel] = useState('small');
  const [transcriptions, setTranscriptions] = useState([]);
  const [modelLoading, setModelLoading] = useState(false);
  
  const ws = useRef(null);
  const reconnectTimeout = useRef(null);
  const pingInterval = useRef(null);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(WS_URL);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        
        // Start ping interval to keep connection alive
        pingInterval.current = setInterval(() => {
          if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'ping' }));
          }
        }, 30000); // Ping every 30 seconds
      };

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'connection':
            setDevice(data.device);
            setCurrentModel(data.model);
            break;
            
          case 'transcription':
            setTranscriptions(prev => [...prev, {
              text: data.text,
              final: data.final,
              timestamp: Date.now()
            }]);
            break;
            
          case 'model_changed':
            setCurrentModel(data.model);
            setDevice(data.device);
            setModelLoading(false);
            break;
            
          case 'status':
            if (data.message.includes('Loading')) {
              setModelLoading(true);
            }
            break;
            
          case 'error':
            console.error('WebSocket error:', data.message);
            setModelLoading(false);
            break;
            
          case 'pong':
            // Server is alive
            break;
            
          default:
            console.log('Unknown message type:', data.type);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        
        // Clear ping interval
        if (pingInterval.current) {
          clearInterval(pingInterval.current);
        }
        
        // Attempt to reconnect after 3 seconds
        reconnectTimeout.current = setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, 3000);
      };
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  }, []);

  const disconnect = useCallback(() => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
    }
    if (pingInterval.current) {
      clearInterval(pingInterval.current);
    }
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
  }, []);

  const sendAudio = useCallback((audioData, format = 'webm') => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({
        type: 'audio',
        data: audioData,
        format: format
      }));
    }
  }, []);

  const changeModel = useCallback((modelName) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      setModelLoading(true);
      ws.current.send(JSON.stringify({
        type: 'change_model',
        model: modelName
      }));
    }
  }, []);

  const clearTranscriptions = useCallback(() => {
    setTranscriptions([]);
  }, []);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    device,
    currentModel,
    transcriptions,
    modelLoading,
    sendAudio,
    changeModel,
    clearTranscriptions
  };
};