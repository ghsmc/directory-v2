import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

interface DropdownTextProps {
  title: string;
  content: string;
}

export function DropdownText({ title, content }: DropdownTextProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 w-full text-left group"
      >
        <p className="font-medium text-gray-900 text-sm lg:text-base">{title}</p>
        <ChevronDown 
          size={16} 
          className={`text-gray-400 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.p
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="text-gray-600 text-sm lg:text-base mt-2 overflow-hidden"
          >
            {content}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}