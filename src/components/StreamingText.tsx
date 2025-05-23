import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

interface StreamingTextProps {
  text: string;
  isDark: boolean;
  isComplete?: boolean;
}

export function StreamingText({ text, isDark, isComplete = false }: StreamingTextProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [chunks, setChunks] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  const parentRef = useRef<HTMLElement | null>(null);
  const scrollTimeoutRef = useRef<NodeJS.Timeout>();
  const isScrollingRef = useRef(false);
  const animationFrameRef = useRef<number>();
  const lastScrollHeightRef = useRef(0);
  const lastScrollTopRef = useRef(0);

  useEffect(() => {
    if (containerRef.current) {
      parentRef.current = containerRef.current.closest('.chat-container');
    }

    const newChunks = text
      .split(/(?<=\n\n|\*\*.*?\*\*|`.*?`|##.*?\n|[.!?]\s+|\|.*?\|\n)/)
      .filter(chunk => chunk.trim().length > 0)
      .map(chunk => chunk.trim());
    
    setChunks(newChunks);
    setCurrentIndex(0);
    setDisplayedText('');
    lastScrollHeightRef.current = 0;
    lastScrollTopRef.current = 0;

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (scrollTimeoutRef.current) {
        clearTimeout(scrollTimeoutRef.current);
      }
    };
  }, [text]);

  const smoothScrollToBottom = () => {
    if (!parentRef.current || isScrollingRef.current) return;

    const container = parentRef.current;
    const currentScrollHeight = container.scrollHeight;
    const currentScrollTop = container.scrollTop;
    const clientHeight = container.clientHeight;
    const maxScroll = currentScrollHeight - clientHeight;
    
    const isAtBottom = Math.abs(currentScrollTop + clientHeight - currentScrollHeight) < 10;
    
    if (currentScrollHeight <= lastScrollHeightRef.current || 
        (!isAtBottom && currentScrollTop < lastScrollTopRef.current)) {
      return;
    }

    isScrollingRef.current = true;
    lastScrollHeightRef.current = currentScrollHeight;
    lastScrollTopRef.current = currentScrollTop;

    const startTime = performance.now();
    const startScroll = currentScrollTop;
    const distance = maxScroll - startScroll;
    const duration = 300;

    const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

    const animateScroll = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      
      if (container.scrollHeight > currentScrollHeight) {
        const newMaxScroll = container.scrollHeight - container.clientHeight;
        container.scrollTop = newMaxScroll;
      } else {
        container.scrollTop = startScroll + (distance * eased);
      }

      if (progress < 1 && !isComplete) {
        animationFrameRef.current = requestAnimationFrame(animateScroll);
      } else {
        isScrollingRef.current = false;
        container.scrollTop = container.scrollHeight - container.clientHeight;
      }
    };

    animationFrameRef.current = requestAnimationFrame(animateScroll);
  };

  useEffect(() => {
    if (currentIndex < chunks.length && !isComplete) {
      const chunk = chunks[currentIndex];
      const isTable = chunk.includes('|');
      const isHeader = chunk.startsWith('##');
      const isParagraphBreak = chunk.includes('\n\n');
      const isSentenceEnd = /[.!?]\s+$/.test(chunk);
      
      const delay = isTable ? 5 :
                   isHeader ? 400 :
                   isParagraphBreak ? 300 :
                   isSentenceEnd ? 200 :
                   chunk.length > 50 ? 100 : 50;

      const timer = setTimeout(() => {
        setDisplayedText(prev => prev + chunks[currentIndex]);
        setCurrentIndex(prev => prev + 1);

        if (scrollTimeoutRef.current) {
          clearTimeout(scrollTimeoutRef.current);
        }

        scrollTimeoutRef.current = setTimeout(() => {
          if (parentRef.current) {
            const container = parentRef.current;
            const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
            
            if (isNearBottom || currentIndex === 0) {
              smoothScrollToBottom();
            }
          }
        }, 16);
      }, delay);

      return () => {
        clearTimeout(timer);
        if (scrollTimeoutRef.current) {
          clearTimeout(scrollTimeoutRef.current);
        }
      };
    }
  }, [currentIndex, chunks, isComplete]);

  useEffect(() => {
    if (isComplete) {
      setDisplayedText(text);
      requestAnimationFrame(() => {
        if (parentRef.current) {
          parentRef.current.scrollTop = parentRef.current.scrollHeight;
        }
      });
    }
  }, [isComplete, text]);

  const markdownComponents = {
    p: ({ children }) => (
      <div className={`
        text-[14px] leading-relaxed m-0 transform-gpu
        ${isDark ? 'text-white/90' : 'text-gray-900'}
      `}>
        {children}
      </div>
    ),
    strong: ({ children }) => (
      <span className={`
        font-semibold transform-gpu
        ${isDark ? 'text-white' : 'text-gray-900'}
      `}>
        {children}
      </span>
    ),
    h2: ({ children }) => (
      <div className={`
        text-base font-bold mt-3 mb-2 flex items-center gap-2 transform-gpu
        ${isDark ? 'text-white' : 'text-gray-900'}
      `}>
        {children}
      </div>
    ),
    ul: ({ children }) => (
      <div className="mt-2 space-y-1.5 transform-gpu">
        {children}
      </div>
    ),
    li: ({ children }) => (
      <div className={`
        flex items-start gap-2 text-[14px] leading-relaxed transform-gpu
        ${isDark ? 'text-white/90' : 'text-gray-900'}
      `}>
        <span className="w-1.5 h-1.5 rounded-full bg-current flex-shrink-0 mt-2" />
        <span>{children}</span>
      </div>
    ),
    table: ({ children }) => (
      <div className="table-container">
        <table>{children}</table>
      </div>
    ),
    thead: ({ children }) => <thead>{children}</thead>,
    tbody: ({ children }) => <tbody>{children}</tbody>,
    tr: ({ children }) => <tr>{children}</tr>,
    th: ({ children }) => <th>{children}</th>,
    td: ({ children }) => <td>{children}</td>
  };

  return (
    <div ref={containerRef} className="prose prose-sm max-w-none overflow-hidden will-change-transform">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
        className="transform-gpu"
      >
        <ReactMarkdown components={markdownComponents}>
          {displayedText}
        </ReactMarkdown>
        {!isComplete && currentIndex < chunks.length && (
          <motion.span
            initial={{ opacity: 0.3 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, repeat: Infinity, repeatType: "reverse" }}
            className={`ml-0.5 ${isDark ? 'text-white/60' : 'text-gray-600'}`}
          >
            ▋
          </motion.span>
        )}
      </motion.div>
    </div>
  );
}