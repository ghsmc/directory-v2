import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Send, X } from 'lucide-react';

interface AIChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialQuery?: string;
}

const suggestedResponses = [
  "Tell me more about the salary range",
  "What skills are required?",
  "Show me similar roles",
  "Which companies are hiring?",
];

export function AIChatModal({ isOpen, onClose, initialQuery }: AIChatModalProps) {
  const [messages, setMessages] = useState<Message[]>([{
    role: 'assistant',
    content: initialQuery 
      ? `I see you're interested in "${initialQuery}". Let me help you find what you're looking for.`
      : "Hi! I'm Milo, your AI assistant. I can help you discover professionals based on your interests and requirements. What kind of people are you looking to connect with?"
  }]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = { 
        role: 'assistant' as const, 
        content: "I'll help you find the right opportunities. Could you tell me more about what specific aspects interest you?" 
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
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
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, y: '100%' }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-x-0 bottom-20 md:bottom-6 md:right-6 md:left-auto md:w-[400px] bg-white rounded-t-xl md:rounded-xl shadow-xl z-50 overflow-hidden max-h-[80vh] md:max-h-[600px]"
          >
            <div className="p-4 border-b border-gray-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <img
                  src="/logo.png"
                  alt="Milo"
                  className="w-12 h-12 rounded-lg object-contain"
                />
                <div>
                  <h3 className="font-medium text-gray-900">Chat with Milo</h3>
                  <p className="text-xs text-gray-500">AI-powered discovery</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-1 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="h-[400px] overflow-y-auto p-4 space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`
                      max-w-[80%] rounded-lg px-4 py-2
                      ${message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                      }
                    `}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              {messages.length === 1 && (
                <div className="mt-4 space-y-2">
                  {suggestedResponses.map((response, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setInput(response);
                        handleSubmit({ preventDefault: () => {} } as React.FormEvent);
                      }}
                      className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      {response}
                    </button>
                  ))}
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="p-4 border-t border-gray-200">
              <div className="relative">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Message Milo..."
                  rows={1}
                  className="w-full pr-10 py-2 pl-3 bg-gray-50 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder:text-gray-500"
                />
                <button
                  type="submit"
                  disabled={!input.trim()}
                  onClick={handleSubmit}
                  className={`
                    absolute right-2 top-1/2 -translate-y-1/2
                    p-1.5 rounded-lg transition-colors duration-200
                    ${input.trim()
                      ? 'text-blue-600 hover:bg-blue-50'
                      : 'text-gray-400'
                    }
                  `}
                >
                  <Send size={18} />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}