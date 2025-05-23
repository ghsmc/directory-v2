import React, { useState, useRef, useEffect } from 'react';
import { Send, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSend: (message: string) => void;
  isDark: boolean;
}

export function ChatModal({ isOpen, onClose, onSend, isDark }: ChatModalProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (isOpen && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isOpen]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          className="fixed bottom-0 inset-x-0 p-4 z-50"
        >
          <div className="max-w-4xl mx-auto">
            <motion.div
              className={`
                rounded-xl shadow-lg overflow-hidden
                ${isDark ? 'glass' : 'bg-white'}
              `}
            >
              <div className={`
                p-4 flex items-center justify-between border-b
                ${isDark ? 'border-white/10' : 'border-gray-100'}
              `}>
                <h3 className={`
                  font-medium
                  ${isDark ? 'text-white/90' : 'text-gray-900'}
                `}>
                  Continue the conversation
                </h3>
                <button
                  onClick={onClose}
                  className={`
                    p-1 rounded-lg transition-colors duration-200
                    ${isDark
                      ? 'hover:bg-white/10 text-white/60'
                      : 'hover:bg-gray-100 text-gray-500'
                    }
                  `}
                >
                  <X size={16} />
                </button>
              </div>
              
              <form onSubmit={handleSubmit} className="p-4">
                <div className="relative">
                  <textarea
                    ref={textareaRef}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    rows={3}
                    className={`
                      w-full px-4 py-3 rounded-lg resize-none
                      ${isDark
                        ? 'bg-white/5 text-white/90 placeholder:text-white/40'
                        : 'bg-gray-50 text-gray-900 placeholder:text-gray-400'
                      }
                      focus:outline-none
                    `}
                  />
                  <button
                    type="submit"
                    disabled={!message.trim()}
                    className={`
                      absolute right-3 bottom-3
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
            </motion.div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}