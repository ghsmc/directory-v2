import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Square } from 'lucide-react';

interface ChatInputProps {
  isDark: boolean;
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  onStop?: () => void;
  isLoading?: boolean;
  isGenerating?: boolean;
  isStreaming?: boolean;
}

export function ChatInput({
  isDark,
  value,
  onChange,
  onSend,
  onStop,
  isLoading = false,
  isGenerating = false,
  isStreaming = false
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isDisabled = isLoading || isGenerating || isStreaming;
  const [localValue, setLocalValue] = useState(value);
  const resizeTimeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleResize = () => {
    if (!textareaRef.current) return;

    if (resizeTimeoutRef.current) {
      clearTimeout(resizeTimeoutRef.current);
    }

    resizeTimeoutRef.current = setTimeout(() => {
      const textarea = textareaRef.current;
      if (!textarea) return;

      textarea.style.height = 'auto';
      // Reduced max height for mobile
      const maxHeight = window.innerWidth < 768 ? 40 : 120;
      textarea.style.height = `${Math.min(textarea.scrollHeight, maxHeight)}px`;
    }, 10);
  };

  useEffect(() => {
    handleResize();
  }, [localValue]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    onChange(newValue);
  };

  const handleSubmit = () => {
    if (!isDisabled && localValue.trim()) {
      onSend();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    return () => {
      if (resizeTimeoutRef.current) {
        clearTimeout(resizeTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="fixed bottom-0 left-0 right-0 z-20 md:left-64 pb-safe">
      <div className="px-2 sm:px-4 pb-2 sm:pb-4">
        <div className="relative mx-auto max-w-[44rem]">
          <div 
            className={`
              relative rounded-xl border
              ${isDark 
                ? 'bg-[#1A1C1E] border-white/10' 
                : 'bg-white border-gray-200'
              }
            `}
          >
            <div className="px-3 pt-1.5 pb-1 sm:pt-2 sm:pb-1.5">
              <textarea
                ref={textareaRef}
                value={localValue}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                disabled={isDisabled}
                placeholder="Message Milo..."
                rows={1}
                className={`
                  w-full resize-none focus:outline-none
                  text-[14px] leading-[1.4] min-h-[24px]
                  ${isDark 
                    ? 'bg-transparent text-white/90 placeholder:text-white/40 placeholder:text-[14px]' 
                    : 'bg-transparent text-gray-900 placeholder:text-gray-500 placeholder:text-[14px]'
                  }
                  ${isDisabled ? 'cursor-not-allowed' : ''}
                `}
                style={{
                  fontFamily: 'inherit',
                  fontSize: '14px',
                  lineHeight: '1.4'
                }}
              />
            </div>

            <div className="px-3 pb-1.5 sm:pb-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={`text-[10px] hidden sm:inline ${isDark ? 'text-white/30' : 'text-gray-400'}`}>
                  Press ⏎ to send
                </span>
              </div>

              <button
                onClick={() => {
                  if (isLoading) {
                    onStop?.();
                  } else {
                    handleSubmit();
                  }
                }}
                disabled={!localValue.trim() || isDisabled}
                className={`
                  p-1.5 rounded-lg transition-all duration-200
                  ${isDisabled
                    ? isDark
                      ? 'bg-gray-900 text-white cursor-not-allowed'
                      : 'bg-gray-900 text-white cursor-not-allowed'
                    : localValue.trim()
                      ? isDark
                        ? 'bg-white/10 text-white hover:bg-white/20'
                        : 'bg-gray-900 text-white hover:bg-gray-800'
                      : isDark
                        ? 'text-white/20'
                        : 'text-gray-300'
                  }
                `}
              >
                {isDisabled ? (
                  <motion.div
                    initial={{ scale: 0.8 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Square size={14} fill="currentColor" />
                  </motion.div>
                ) : (
                  <Send size={14} />
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}