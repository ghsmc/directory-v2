import React, { useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface SearchModalProps {
  query: string;
  isDark: boolean;
  onQueryChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function SearchModal({ query, isDark, onQueryChange, onSubmit }: SearchModalProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === '/' && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        textareaRef.current?.focus();
      }
      
      if (e.key === 'Escape') {
        textareaRef.current?.blur();
        onQueryChange('');
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [onQueryChange]);

  const handleTextareaInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = e.target;
    onQueryChange(textarea.value);
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (query.trim()) {
        onSubmit(e);
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -10, rotateX: -5 }}
      animate={{ opacity: 1, y: 0, rotateX: 0 }}
      exit={{ opacity: 0, y: -10, rotateX: -5 }}
      transition={{ duration: 0.2, type: 'spring', stiffness: 300, damping: 25 }}
      className="fixed top-4 inset-x-0 mx-auto z-50 px-4 max-w-[760px]"
    >
      <form 
        onSubmit={onSubmit}
        className={`
          search-modal relative
          ${isDark ? 'bg-[#40414F] border-[#3E3F4B]' : 'bg-white border-[#ECECF1]'}
          border rounded-xl backdrop-blur-sm
          transform-gpu perspective-1000
        `}
      >
        <textarea
          ref={textareaRef}
          value={query}
          onChange={handleTextareaInput}
          onKeyDown={handleKeyDown}
          placeholder="Search for opportunities... (Press / to focus)"
          rows={1}
          className={`
            w-full px-4 py-[14px] pr-12
            search-input resize-none overflow-hidden rounded-xl
            ${isDark 
              ? 'bg-[#40414F] text-[#EFEFEF] placeholder-[#8E8EA0]' 
              : 'bg-white text-[#333333] placeholder-[#8E8EA0]'
            }
            focus:outline-none text-[16px]
            transform-gpu transition-transform duration-200
          `}
        />
        <button 
          type="submit"
          disabled={!query.trim()}
          className={`
            send-button absolute right-3 top-1/2 -translate-y-1/2
            p-2 rounded-lg transition-all duration-200 transform-gpu
            ${query.trim()
              ? `${isDark ? 'text-white bg-gpt-green' : 'text-white bg-gpt-green'} hover:opacity-80`
              : isDark ? 'text-[#8E8EA0]' : 'text-[#ECECF1]'
            }
          `}
        >
          <Send size={20} className={query.trim() ? 'transform rotate-90' : ''} />
        </button>
      </form>
    </motion.div>
  );
}