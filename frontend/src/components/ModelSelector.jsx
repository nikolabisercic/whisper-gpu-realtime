import React from 'react';
import { ChevronDown, Cpu, Zap } from 'lucide-react';

const ModelSelector = ({ currentModel, onModelChange, isLoading, device }) => {
  const models = [
    { id: 'tiny', name: 'Tiny', speed: '⚡⚡⚡⚡⚡', accuracy: '★★', description: 'Fastest, testing' },
    { id: 'base', name: 'Base', speed: '⚡⚡⚡⚡', accuracy: '★★★', description: 'Fast, daily use' },
    { id: 'small', name: 'Small', speed: '⚡⚡⚡', accuracy: '★★★★', description: 'Balanced, recommended' },
    { id: 'medium', name: 'Medium', speed: '⚡⚡', accuracy: '★★★★★', description: 'Most accurate' },
  ];

  return (
    <div className="w-full max-w-md">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Model Selection
      </label>
      <div className="relative">
        <select
          value={currentModel}
          onChange={(e) => onModelChange(e.target.value)}
          disabled={isLoading}
          className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-4 py-3 pr-10 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name} - {model.description}
            </option>
          ))}
        </select>
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <ChevronDown className="w-5 h-5 text-gray-500" />
        </div>
      </div>
      
      {/* Model info display */}
      <div className="mt-3 flex items-center justify-between text-sm">
        <div className="flex items-center gap-4">
          {models.find(m => m.id === currentModel) && (
            <>
              <span className="text-gray-600">
                Speed: {models.find(m => m.id === currentModel).speed}
              </span>
              <span className="text-gray-600">
                Accuracy: {models.find(m => m.id === currentModel).accuracy}
              </span>
            </>
          )}
        </div>
        <div className="flex items-center gap-1">
          {device === 'cuda' ? (
            <>
              <Zap className="w-4 h-4 text-green-500" />
              <span className="text-green-600 font-medium">GPU</span>
            </>
          ) : (
            <>
              <Cpu className="w-4 h-4 text-blue-500" />
              <span className="text-blue-600 font-medium">CPU</span>
            </>
          )}
        </div>
      </div>
      
      {isLoading && (
        <div className="mt-2 text-sm text-gray-500 animate-pulse">
          Loading model...
        </div>
      )}
    </div>
  );
};

export default ModelSelector;