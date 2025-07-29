import { useState, useCallback, useRef } from 'react';

export const useAudioRecorderPCM = (onDataAvailable) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Audio context and nodes
  const audioContext = useRef(null);
  const stream = useRef(null);
  const source = useRef(null);
  const processor = useRef(null);
  const sendInterval = useRef(null);
  const audioBuffer = useRef([]);

  // Convert Float32Array to base64
  const float32ToBase64 = (float32Array) => {
    const buffer = new ArrayBuffer(float32Array.length * 4);
    const view = new Float32Array(buffer);
    view.set(float32Array);
    
    // Convert ArrayBuffer to base64
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  };

  const startRecording = useCallback(async () => {
    try {
      // Request microphone access
      stream.current = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });

      // Create audio context with specific sample rate
      audioContext.current = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000
      });

      // Create source from stream
      source.current = audioContext.current.createMediaStreamSource(stream.current);
      
      // Create script processor (4096 samples buffer)
      processor.current = audioContext.current.createScriptProcessor(4096, 1, 1);
      
      // Accumulate audio data
      processor.current.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        // Copy data to avoid reference issues
        audioBuffer.current.push(...inputData);
      };

      // Connect nodes
      source.current.connect(processor.current);
      processor.current.connect(audioContext.current.destination);

      // Send accumulated audio every 250ms
      sendInterval.current = setInterval(() => {
        if (audioBuffer.current.length > 0) {
          // Create Float32Array from buffer
          const audioData = new Float32Array(audioBuffer.current);
          audioBuffer.current = []; // Clear buffer
          
          // Convert to base64 and send
          const base64Audio = float32ToBase64(audioData);
          onDataAvailable(base64Audio, 'pcm');
        }
      }, 250);

      setIsRecording(true);
      setIsProcessing(false);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  }, [onDataAvailable]);

  const stopRecording = useCallback(() => {
    if (isRecording) {
      // Clear send interval
      if (sendInterval.current) {
        clearInterval(sendInterval.current);
        sendInterval.current = null;
      }

      // Send any remaining audio
      if (audioBuffer.current.length > 0) {
        const audioData = new Float32Array(audioBuffer.current);
        const base64Audio = float32ToBase64(audioData);
        onDataAvailable(base64Audio, 'pcm');
        audioBuffer.current = [];
      }

      // Disconnect audio nodes
      if (processor.current) {
        processor.current.disconnect();
        processor.current = null;
      }
      if (source.current) {
        source.current.disconnect();
        source.current = null;
      }

      // Close audio context
      if (audioContext.current) {
        audioContext.current.close();
        audioContext.current = null;
      }

      // Stop all tracks
      if (stream.current) {
        stream.current.getTracks().forEach(track => track.stop());
        stream.current = null;
      }

      setIsRecording(false);
      setIsProcessing(true);

      // Simulate processing time
      setTimeout(() => {
        setIsProcessing(false);
      }, 1000);
    }
  }, [isRecording, onDataAvailable]);

  const toggleRecording = useCallback(() => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }, [isRecording, startRecording, stopRecording]);

  return {
    isRecording,
    isProcessing,
    startRecording,
    stopRecording,
    toggleRecording
  };
};