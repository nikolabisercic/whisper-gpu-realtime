import { useState, useCallback, useRef } from 'react';

export const useAudioRecorder = (onDataAvailable) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorder = useRef(null);
  const stream = useRef(null);

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

      // Create MediaRecorder with webm format
      const options = {
        mimeType: 'audio/webm;codecs=opus'
      };

      mediaRecorder.current = new MediaRecorder(stream.current, options);

      // Handle data available event
      mediaRecorder.current.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          // Convert blob to base64
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64data = reader.result;
            onDataAvailable(base64data, 'webm');
          };
          reader.readAsDataURL(event.data);
        }
      };

      // Start recording with time slicing
      mediaRecorder.current.start(250); // Send data every 250ms
      setIsRecording(true);
      setIsProcessing(false);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  }, [onDataAvailable]);

  const stopRecording = useCallback(() => {
    if (mediaRecorder.current && mediaRecorder.current.state !== 'inactive') {
      mediaRecorder.current.stop();
      setIsRecording(false);
      setIsProcessing(true);

      // Stop all tracks
      if (stream.current) {
        stream.current.getTracks().forEach(track => track.stop());
      }

      // Simulate processing time
      setTimeout(() => {
        setIsProcessing(false);
      }, 1000);
    }
  }, []);

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