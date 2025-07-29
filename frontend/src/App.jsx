import React, { useEffect } from 'react';
import ModelSelector from './components/ModelSelector';
import RecordButton from './components/RecordButton';
import TranscriptionBox from './components/TranscriptionBox';
import StatusIndicator from './components/StatusIndicator';
import { useWebSocket } from './hooks/useWebSocket';
import { useAudioRecorderPCM } from './hooks/useAudioRecorderPCM';

function App() {
  const {
    isConnected,
    device,
    currentModel,
    transcriptions,
    modelLoading,
    sendAudio,
    changeModel,
    clearTranscriptions
  } = useWebSocket();

  const {
    isRecording,
    isProcessing,
    toggleRecording
  } = useAudioRecorderPCM(sendAudio);

  // Keyboard shortcut for recording (spacebar)
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.code === 'Space' && !e.repeat && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        toggleRecording();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [toggleRecording]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Speech to Text</h1>
              <p className="text-sm text-gray-600 mt-1">
                Real-time transcription powered by Whisper
              </p>
            </div>
            <StatusIndicator
              isConnected={isConnected}
              device={device}
              modelLoading={modelLoading}
            />
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left column - Controls */}
          <div className="lg:col-span-1 space-y-8">
            {/* Model selector */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <ModelSelector
                currentModel={currentModel}
                onModelChange={changeModel}
                isLoading={modelLoading}
                device={device}
              />
            </div>

            {/* Record button */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 flex items-center justify-center">
              <RecordButton
                isRecording={isRecording}
                isProcessing={isProcessing}
                onToggleRecording={toggleRecording}
              />
            </div>

            {/* Instructions */}
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <h3 className="font-medium text-blue-900 mb-2">Quick Tips</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Click the button or press Space to record</li>
                <li>• Speak clearly into your microphone</li>
                <li>• Transcription appears in real-time</li>
                <li>• Click Copy to save your text</li>
              </ul>
            </div>
          </div>

          {/* Right column - Transcription */}
          <div className="lg:col-span-2">
            <TranscriptionBox
              transcriptions={transcriptions}
              onClear={clearTranscriptions}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Powered by faster-whisper with GPU acceleration
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;