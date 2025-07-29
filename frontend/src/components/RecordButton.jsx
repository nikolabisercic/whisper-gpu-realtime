import React from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import clsx from 'clsx';

const RecordButton = ({ isRecording, isProcessing, onToggleRecording }) => {
  const buttonClasses = clsx(
    'relative w-32 h-32 rounded-full flex items-center justify-center transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-opacity-50',
    {
      'bg-gray-200 hover:bg-gray-300 focus:ring-gray-400': !isRecording && !isProcessing,
      'bg-red-500 hover:bg-red-600 focus:ring-red-400': isRecording,
      'bg-blue-500 focus:ring-blue-400': isProcessing,
    }
  );

  const pulseClasses = clsx(
    'absolute inset-0 rounded-full animate-ping',
    {
      'bg-red-400 opacity-75': isRecording,
      'hidden': !isRecording,
    }
  );

  return (
    <div className="flex flex-col items-center gap-4">
      <button
        onClick={onToggleRecording}
        disabled={isProcessing}
        className={buttonClasses}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {/* Pulse animation for recording */}
        <div className={pulseClasses}></div>
        
        {/* Icon */}
        <div className="relative z-10">
          {isProcessing ? (
            <Loader2 className="w-12 h-12 text-white animate-spin" />
          ) : isRecording ? (
            <Square className="w-10 h-10 text-white" />
          ) : (
            <Mic className="w-12 h-12 text-gray-700" />
          )}
        </div>
      </button>
      
      {/* Status text */}
      <div className="text-center">
        <p className="text-lg font-medium text-gray-900">
          {isProcessing ? 'Processing...' : isRecording ? 'Recording...' : 'Click to record'}
        </p>
        <p className="text-sm text-gray-500 mt-1">
          {!isRecording && !isProcessing && 'Or press spacebar'}
        </p>
      </div>
    </div>
  );
};

export default RecordButton;