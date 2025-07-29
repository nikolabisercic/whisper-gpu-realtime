import React from 'react';
import { Wifi, WifiOff, Zap, Cpu } from 'lucide-react';
import clsx from 'clsx';

const StatusIndicator = ({ isConnected, device, modelLoading }) => {
  return (
    <div className="flex items-center gap-4 text-sm">
      {/* Connection status */}
      <div className="flex items-center gap-2">
        {isConnected ? (
          <>
            <Wifi className="w-4 h-4 text-green-500" />
            <span className="text-green-600">Connected</span>
          </>
        ) : (
          <>
            <WifiOff className="w-4 h-4 text-red-500" />
            <span className="text-red-600">Disconnected</span>
          </>
        )}
      </div>

      {/* Device status */}
      <div className="flex items-center gap-2">
        {device === 'cuda' ? (
          <>
            <Zap className="w-4 h-4 text-yellow-500" />
            <span className="text-gray-700">GPU Acceleration</span>
          </>
        ) : (
          <>
            <Cpu className="w-4 h-4 text-blue-500" />
            <span className="text-gray-700">CPU Mode</span>
          </>
        )}
      </div>

      {/* Model loading indicator */}
      {modelLoading && (
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-gray-600">Loading model...</span>
        </div>
      )}
    </div>
  );
};

export default StatusIndicator;