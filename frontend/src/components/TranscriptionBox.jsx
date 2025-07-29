import React, { useRef, useEffect, useState } from 'react';
import { Copy, Check, Trash2 } from 'lucide-react';

const TranscriptionBox = ({ transcriptions, onClear }) => {
  const [copied, setCopied] = useState(false);
  const scrollRef = useRef(null);

  // Auto-scroll to bottom when new transcriptions come in
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcriptions]);

  const handleCopy = async () => {
    const text = transcriptions.map(t => t.text).join(' ');
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const fullText = transcriptions.map(t => t.text).join(' ');
  const wordCount = fullText.split(/\s+/).filter(word => word.length > 0).length;
  const charCount = fullText.length;

  return (
    <div className="w-full max-w-4xl">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-medium text-gray-900">Transcription</h3>
        <div className="flex items-center gap-2">
          {transcriptions.length > 0 && (
            <>
              <button
                onClick={onClear}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                aria-label="Clear transcription"
              >
                <Trash2 className="w-5 h-5" />
              </button>
              <button
                onClick={handleCopy}
                className="flex items-center gap-2 px-3 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                aria-label="Copy transcription"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4 text-green-600" />
                    <span className="text-sm font-medium text-green-600">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    <span className="text-sm font-medium">Copy</span>
                  </>
                )}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Transcription area */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        <div
          ref={scrollRef}
          className="p-6 min-h-[300px] max-h-[500px] overflow-y-auto"
        >
          {transcriptions.length === 0 ? (
            <p className="text-gray-400 text-center">
              Your transcription will appear here...
            </p>
          ) : (
            <div className="space-y-2">
              {transcriptions.map((item, index) => (
                <span
                  key={index}
                  className={`inline ${
                    item.final ? 'text-gray-900' : 'text-gray-500'
                  }`}
                >
                  {item.text}{' '}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Footer with stats */}
        {transcriptions.length > 0 && (
          <div className="border-t border-gray-200 px-6 py-3 bg-gray-50 rounded-b-lg">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <div className="flex items-center gap-4">
                <span>{wordCount} words</span>
                <span>{charCount} characters</span>
              </div>
              <span>{transcriptions.length} segments</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TranscriptionBox;