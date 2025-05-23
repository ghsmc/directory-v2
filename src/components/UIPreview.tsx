import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ArrowUpRight, Briefcase, FlaskRound as Flask, Users, Check, ArrowRight } from 'lucide-react';
import { StreamingText } from './StreamingText';

interface Message {
  role: 'assistant' | 'user';
  content: string;
  isComplete?: boolean;
}

const categories = [
  {
    id: 'labs',
    icon: Flask,
    emoji: '🔬',
    title: 'Labs',
    query: "Looking for biology research labs working on CRISPR",
    response: "Hey! I found some interesting labs working on CRISPR. The **MIT Broad Institute** looks particularly strong for gene editing work. Would you prefer a more computational or experimental focus?",
    followUpTags: [
      "Computational focus",
      "Experimental work",
      "Both"
    ]
  },
  {
    id: 'jobs',
    icon: Briefcase,
    emoji: '💼',
    title: 'Jobs',
    query: "Looking for software engineering internships in NYC",
    response: "**Bloomberg** might be a good match if you like the more mathematical side of software engineering. They do a lot of interesting work with financial data and real-time systems. How important is the creative aspect of engineering to you?",
    followUpTags: [
      "Very important",
      "Somewhat important",
      "Not important"
    ]
  },
  {
    id: 'clubs',
    icon: Users,
    emoji: '👥',
    title: 'Clubs',
    query: "What tech and entrepreneurship clubs are active?",
    response: "**Code4Good** could be interesting - they work on real projects for nonprofits. It's a great way to build your portfolio while making an impact. Are you more interested in the coding or the social impact side?",
    followUpTags: [
      "Coding focus",
      "Social impact",
      "Both equally"
    ]
  }
];

const results = {
  labs: [
    {
      name: "MIT Broad Institute",
      logo: "https://img.logo.dev/broad.mit.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Leading CRISPR research lab focused on genomic engineering and therapeutic applications",
      location: "Cambridge, MA",
      status: "Accepting Applications",
      tags: ["CRISPR", "Gene Editing", "Molecular Biology"],
      matchScore: "98%",
      deadline: "Mar 15"
    },
    {
      name: "Stanford Gene Lab",
      logo: "https://img.logo.dev/stanford.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Innovative research in genetic engineering and synthetic biology",
      location: "Stanford, CA",
      status: "Open Positions",
      tags: ["Synthetic Biology", "Gene Therapy", "Bioinformatics"],
      matchScore: "95%",
      deadline: "Apr 1"
    }
  ],
  jobs: [
    {
      name: "Bloomberg",
      logo: "https://img.logo.dev/bloomberg.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Software Engineering Internship focused on financial technology and real-time systems",
      location: "New York, NY",
      status: "Actively Hiring",
      salary: "$150,000 - $200,000",
      tags: ["Financial Tech", "C++", "Real-time Systems"],
      matchScore: "96%",
      deadline: "Feb 28"
    },
    {
      name: "Google NYC",
      logo: "https://img.logo.dev/google.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Summer internship program in various engineering teams",
      location: "New York, NY",
      status: "Applications Open",
      salary: "$175,000 - $225,000",
      tags: ["Cloud", "Machine Learning", "Full Stack"],
      matchScore: "94%",
      deadline: "Mar 31"
    }
  ],
  clubs: [
    {
      name: "Code4Good",
      logo: "https://img.logo.dev/yale.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Student-run organization developing software solutions for nonprofits",
      location: "Remote",
      status: "Recruiting",
      tags: ["Social Impact", "Web Dev", "Open Source"],
      matchScore: "97%",
      deadline: "Ongoing"
    },
    {
      name: "Tech Entrepreneurs",
      logo: "https://img.logo.dev/yale.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      description: "Club focused on startup development and innovation",
      location: "Hybrid",
      status: "Open to All",
      tags: ["Startups", "Innovation", "Networking"],
      matchScore: "93%",
      deadline: "Rolling"
    }
  ]
};

interface UIPreviewProps {
  onGetStarted?: () => void;
}

export function UIPreview({ onGetStarted }: UIPreviewProps) {
  const [currentCategoryIndex, setCurrentCategoryIndex] = useState(0);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [appliedItems, setAppliedItems] = useState<Set<string>>(new Set());
  const [isHovered, setIsHovered] = useState(false);

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
      setAppliedItems(new Set()); // Reset applied items when category changes
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
            {isApplied
              ? currentCategory.id === 'clubs' ? 'Joined' : 'Applied'
              : currentCategory.id === 'clubs' ? 'Join' : 'Apply'
            }
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
                    {result.deadline && (
                      <div className="flex items-center gap-1">
                        <span className="text-[11px] text-gray-500">
                          Due {result.deadline}
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

  return (
    <div 
      className="relative rounded-2xl border border-gray-200 bg-white shadow-2xl overflow-hidden min-h-[600px] sm:min-h-[500px]"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <AnimatePresence>
        {isHovered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center cursor-pointer"
            onClick={onGetStarted}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="flex flex-col items-center gap-4"
            >
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ 
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                <ArrowRight size={40} className="text-white/90" />
              </motion.div>
              <button
                className="px-6 py-3 bg-white rounded-lg text-gray-900 font-medium text-lg
                  hover:bg-gray-50 transition-colors duration-200"
              >
                Start Discovering
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex items-center gap-3 border-b border-gray-100 px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/20 to-indigo-500/20 rounded-lg blur-sm" />
            <img 
              src="https://gmccain.com/milo.png"
              alt="Milo"
              className="relative w-8 h-8 rounded-lg"
            />
          </div>
          <div>
            <div className="text-sm font-medium text-gray-900">Milo AI</div>
            <div className="text-xs text-gray-500">Powered by advanced AI</div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:grid sm:grid-cols-2 h-[calc(100%-129px)]">
        <div className="border-b sm:border-b-0 sm:border-r border-gray-100 overflow-y-auto hide-scrollbar">
          <div className="px-4 py-3 space-y-6">
            {messages.map((message, index) => (
              <div 
                key={index}
                className={`flex items-start gap-3 ${
                  message.role === 'user' ? 'justify-end' : ''
                }`}
              >
                {message.role === 'assistant' && (
                  <img 
                    src="https://gmccain.com/milo.png"
                    alt="Milo"
                    className="w-7 h-7 rounded-lg flex-shrink-0 mt-0.5"
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

        <div className="overflow-y-auto hide-scrollbar bg-white">
          <div className="sticky top-0 bg-white border-b border-gray-100 px-4 py-2 flex items-center justify-center gap-2">
            <span className="text-xl">{currentCategory.emoji}</span>
            <h2 className="text-sm font-medium text-gray-900">{currentCategory.title}</h2>
          </div>

          <div className="p-2">
            {renderResults()}
          </div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 px-4 py-3 border-t border-gray-100 bg-white">
        <div className="flex items-center gap-3 rounded-xl border border-gray-200 bg-gray-50 px-4 py-2.5">
          <input
            type="text"
            placeholder="Message Milo..."
            className="flex-1 bg-transparent text-[14px] outline-none placeholder:text-gray-400"
          />
          <button className="p-1.5 rounded-lg hover:bg-gray-200 transition-colors">
            <ArrowUpRight size={18} className="text-gray-600" />
          </button>
        </div>
      </div>
    </div>
  );
}