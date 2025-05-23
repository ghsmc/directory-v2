import React, { useState } from 'react';
import { Send } from 'lucide-react';

interface ChatBarProps {
  isDark: boolean;
  onSend: (message: string) => void;
}

export function ChatBar({ isDark, onSend }: ChatBarProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <div className={`
      fixed bottom-0 left-64 right-0 p-6
      ${isDark ? 'bg-gradient-to-t from-black via-black/90 to-transparent' : 'bg-gradient-to-t from-white via-white/90 to-transparent'}
    `}>
      <div className="max-w-4xl mx-auto">
        <form 
          onSubmit={handleSubmit}
          className={`
            relative rounded-xl overflow-hidden
            ${isDark ? 'bg-[#1C1C1F] border border-white/10' : 'bg-white shadow-lg'}
          `}
        >
          <div className="p-4">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask Milo AI about this job..."
              rows={1}
              className={`
                w-full px-4 py-3 rounded-lg resize-none
                ${isDark
                  ? 'bg-white/5 text-white/90 placeholder:text-white/40'
                  : 'bg-gray-50 text-gray-900 placeholder:text-gray-500'
                }
                focus:outline-none
              `}
            />
            <button
              type="submit"
              disabled={!message.trim()}
              className={`
                absolute right-6 top-1/2 -translate-y-1/2
                p-2 rounded-lg transition-all duration-200
                ${message.trim()
                  ? `${isDark ? 'bg-white/10 text-white' : 'bg-gray-900 text-white'} hover:opacity-80`
                  : `${isDark ? 'text-white/20' : 'text-gray-300'}`
                }
              `}
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}