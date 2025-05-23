import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ArrowUpRight, Briefcase, Building2, Check } from 'lucide-react';
import { StreamingText } from './StreamingText';
import { ChatInput } from './ChatInput';

interface Message {
  role: 'assistant' | 'user';
  content: string;
  isComplete?: boolean;
}

const categories = [
  {
    id: 'jobs',
    icon: Briefcase,
    emoji: '💼',
    title: 'Jobs',
    query: "Looking for software engineering roles in AI companies",
    response: "Based on your profile, I've found some exciting AI engineering positions. **OpenAI** and **Anthropic** are both actively hiring for roles that match your skills. Would you prefer to focus on research or product development?",
    followUpTags: [
      "Research focused",
      "Product development",
      "Both interests me"
    ]
  },
  {
    id: 'companies',
    icon: Building2,
    emoji: '🏢',
    title: 'Companies',
    query: "Show me AI companies that are hiring",
    response: "I've found several promising AI companies. **Anthropic** and **OpenAI** are leading the field in AI safety and large language models. They offer competitive compensation and strong growth potential. What aspects of these companies interest you most?",
    followUpTags: [
      "AI Safety focus",
      "Technical challenges",
      "Company culture"
    ]
  }
];

const results = {
  jobs: [
    {
      name: "OpenAI",
      logo: "https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "ML Engineer position focused on advancing AI capabilities and safety",
      location: "San Francisco, CA",
      status: "Actively Hiring",
      salary: "$200,000 - $350,000",
      tags: ["Python", "ML", "AI Safety"],
      matchScore: "96%",
      deadline: "Rolling"
    },
    {
      name: "Anthropic",
      logo: "https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Research Engineer role in AI alignment and safety",
      location: "San Francisco, CA",
      status: "Applications Open",
      salary: "$180,000 - $300,000",
      tags: ["AI Safety", "ML", "Research"],
      matchScore: "94%",
      deadline: "Mar 31"
    }
  ],
  companies: [
    {
      name: "Anthropic",
      logo: "https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Leading AI research company focused on safe and ethical AI development",
      location: "San Francisco, CA",
      status: "Series B",
      valuation: "$4.1B",
      tags: ["AI Safety", "ML Research", "Ethics"],
      matchScore: "95%",
      positions: "45 open roles"
    },
    {
      name: "OpenAI",
      logo: "https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Pioneer in advanced AI systems and language models",
      location: "San Francisco, CA",
      status: "Late Stage",
      valuation: "$80B",
      tags: ["LLMs", "AI Research", "ML"],
      matchScore: "93%",
      positions: "156 open roles"
    }
  ]
};

export function ChatInterface() {
  const [currentCategoryIndex, setCurrentCategoryIndex] = useState(0);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [appliedItems, setAppliedItems] = useState<Set<string>>(new Set());
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      const currentResults = results[categories[currentCategoryIndex].id as keyof typeof results];
      if (currentResults.length > 0) {
        handleApplyClick(currentResults[0].name);
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [currentCategoryIndex]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentCategoryIndex((prev) => (prev + 1) % categories.length);
      setAppliedItems(new Set());
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const category = categories[currentCategoryIndex];
    setMessages([
      { role: 'user', content: category.query },
      { role: 'assistant', content: category.response, isComplete: true }
    ]);
    setIsTyping(false);
  }, [currentCategoryIndex]);

  const handleApplyClick = (itemId: string) => {
    setAppliedItems(prev => {
      const next = new Set(prev);
      next.add(itemId);
      return next;
    });
  };

  const currentCategory = categories[currentCategoryIndex];

  const renderApplyButton = (result: any) => {
    const isApplied = appliedItems.has(result.name);
    
    return (
      <motion.button 
        onClick={() => handleApplyClick(result.name)}
        className={`
          relative px-3 py-1 rounded-lg text-[11px] font-medium
          transition-all duration-300 ease-in-out
          ${isApplied
            ? 'bg-emerald-100 text-emerald-600'
            : 'bg-blue-600 text-white hover:opacity-90'
          }
        `}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <motion.div
          className="flex items-center gap-1"
          initial={false}
        >
          <AnimatePresence mode="popLayout">
            {isApplied && (
              <motion.span
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0, opacity: 0 }}
                transition={{ type: "spring", stiffness: 500, damping: 25 }}
              >
                <Check size={12} />
              </motion.span>
            )}
          </AnimatePresence>
          <motion.span layout>
            {isApplied ? 'Applied' : 'Apply'}
          </motion.span>
        </motion.div>
      </motion.button>
    );
  };

  const renderResults = () => {
    return (
      <div className="p-4 space-y-2">
        {results[currentCategory.id as keyof typeof results].map((result: any, index: number) => (
          <motion.div
            key={result.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.2 }}
            className="p-2.5 bg-white border border-gray-200 rounded-xl hover:border-gray-300 transition-colors"
          >
            <div className="flex items-start gap-3">
              <img 
                src={result.logo}
                alt={result.name}
                className="w-8 h-8 rounded bg-white flex-shrink-0"
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="text-[13px] font-medium text-gray-900 truncate">
                        {result.name}
                      </h3>
                      <ArrowUpRight size={13} className="text-gray-400 flex-shrink-0" />
                    </div>
                    <div className="text-[12px] text-gray-600 line-clamp-2 mt-0.5">
                      {result.description}
                    </div>
                    {result.salary && (
                      <div className="mt-1 text-[13px] font-medium text-emerald-600">
                        {result.salary}
                      </div>
                    )}
                  </div>
                  <div className="flex flex-col items-end flex-shrink-0">
                    <div className="text-[11px] uppercase tracking-wide font-medium text-gray-500">
                      {result.location}
                    </div>
                    <div className="text-[11px] text-gray-500 mt-0.5">
                      {result.status}
                    </div>
                  </div>
                </div>

                <div className="mt-2 flex flex-wrap gap-1">
                  {result.tags.map((tag: string) => (
                    <span
                      key={tag}
                      className="text-[11px] font-medium px-1.5 py-0.5 rounded-full bg-gray-100 text-gray-600"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="mt-2 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1">
                      <div className="px-1.5 py-0.5 rounded-full font-medium text-[11px] bg-emerald-500 text-white">
                        {result.matchScore}
                      </div>
                      <span className="text-[11px] text-gray-500">
                        Match
                      </span>
                    </div>
                    {(result.deadline || result.positions) && (
                      <div className="flex items-center gap-1">
                        <span className="text-[11px] text-gray-500">
                          {result.deadline ? `Due ${result.deadline}` : result.positions}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {renderApplyButton(result)}
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: inputValue }]);
    setInputValue('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "I'll help you find the right opportunities. Could you tell me more about what specific aspects interest you?" 
      }]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="h-screen flex flex-col bg-white overflow-hidden">
      {/* Header */}
      <div className="flex-shrink-0 flex items-center gap-3 border-b border-gray-100 px-4 py-3">
        <div className="flex items-center gap-3 w-full">
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/20 to-indigo-500/20 rounded-lg blur-sm" />
            <img 
              src="/logo_clean.png"
              alt="Milo"
              className="relative w-12 h-12 rounded-lg object-contain"
            />
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-gray-900">Milo AI</div>
            <div className="text-xs text-gray-500">Powered by advanced AI</div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col sm:grid sm:grid-cols-2 min-h-0">
        {/* Chat Messages */}
        <div className="flex-1 border-b sm:border-b-0 sm:border-r border-gray-100 overflow-y-auto hide-scrollbar">
          <div className="px-4 py-3 space-y-6 pb-32 sm:pb-4">
            {messages.map((message, index) => (
              <div 
                key={index}
                className={`flex items-start gap-3 ${
                  message.role === 'user' ? 'justify-end' : ''
                }`}
              >
                {message.role === 'assistant' && (
                  <img 
                    src="/logo_clean.png"
                    alt="Milo"
                    className="w-12 h-12 rounded-lg flex-shrink-0 mt-0.5 object-contain"
                  />
                )}
                <div 
                  className={`
                    ${message.role === 'user' 
                      ? 'bg-gray-100 text-gray-900 rounded-2xl rounded-tr-md px-4 py-2 max-w-[85%]' 
                      : 'flex-1'
                    }
                  `}
                >
                  {index === messages.length - 1 && message.role === 'assistant' ? (
                    <>
                      <StreamingText 
                        text={message.content}
                        isDark={false}
                        isComplete={!isTyping}
                      />
                      {!isTyping && (
                        <div className="mt-3 flex flex-wrap gap-1.5">
                          {currentCategory.followUpTags.map((tag, i) => (
                            <button
                              key={i}
                              onClick={() => {
                                setInputValue(tag);
                                handleSendMessage();
                              }}
                              className="text-[11px] px-2 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors"
                            >
                              {tag}
                            </button>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <p className="text-[14px] leading-relaxed m-0">
                      {message.content}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Results Panel */}
        <div className="hidden sm:block overflow-y-auto hide-scrollbar bg-white">
          <div className="sticky top-0 bg-white border-b border-gray-100 px-4 py-2 flex items-center justify-center gap-2">
            <span className="text-xl">{currentCategory.emoji}</span>
            <h2 className="text-sm font-medium text-gray-900">{currentCategory.title}</h2>
          </div>

          <div className="p-2">
            {renderResults()}
          </div>
        </div>
      </div>

      {/* Chat Input - Fixed at bottom */}
      <div className="flex-shrink-0 fixed bottom-0 left-0 right-0 md:left-[72px] bg-white border-t border-gray-100">
        <div className="max-w-none mx-auto px-4 py-4 pb-safe">
          <ChatInput
            isDark={false}
            value={inputValue}
            onChange={setInputValue}
            onSend={handleSendMessage}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}