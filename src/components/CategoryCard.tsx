import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useSound from 'use-sound';

interface CategoryCardProps {
  id: string;
  label: string;
  icon: React.ElementType;
  description: string;
  isActive: boolean;
  isDark: boolean;
  onClick: () => void;
  recentSearches?: number;
  popularQueries?: string[];
}

export function CategoryCard({
  id,
  label,
  icon: Icon,
  description,
  isActive,
  isDark,
  onClick,
  recentSearches = 0,
  popularQueries = [],
}: CategoryCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [playHover] = useSound('/hover.mp3', { volume: 0.5 });
  const [playSelect] = useSound('/select.mp3', { volume: 0.5 });
  const cardRef = useRef<HTMLDivElement>(null);
  
  const handleClick = (e: React.MouseEvent) => {
    const rect = cardRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const ink = document.createElement('div');
    ink.className = 'ink-effect';
    ink.style.width = ink.style.height = Math.max(rect.width, rect.height) + 'px';
    ink.style.left = (e.clientX - rect.left - rect.width/2) + 'px';
    ink.style.top = (e.clientY - rect.top - rect.height/2) + 'px';
    
    cardRef.current?.appendChild(ink);
    ink.addEventListener('animationend', () => ink.remove());
    
    playSelect();
    onClick();
  };

  const variants = {
    initial: { 
      scale: 1, 
      rotateX: 0, 
      rotateY: 0,
      translateZ: 0 
    },
    hover: { 
      scale: 1.02,
      rotateX: 5,
      rotateY: 5,
      translateZ: 20,
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 20
      }
    },
    tap: { 
      scale: 0.98,
      rotateX: 0,
      rotateY: 0,
      translateZ: 10
    }
  };

  const iconVariants = {
    initial: { 
      scale: 1, 
      rotate: 0, 
      y: 0,
      translateZ: 0 
    },
    hover: { 
      scale: 1.1,
      rotate: 5,
      y: -2,
      translateZ: 30,
      transition: {
        type: "spring",
        stiffness: 400,
        damping: 15
      }
    }
  };

  return (
    <motion.div
      ref={cardRef}
      variants={variants}
      initial="initial"
      whileHover="hover"
      whileTap="tap"
      onHoverStart={() => {
        setIsHovered(true);
        playHover();
      }}
      onHoverEnd={() => setIsHovered(false)}
      onClick={handleClick}
      className={`
        relative overflow-hidden p-6 rounded-xl text-center category-card
        transform-gpu transition-all duration-300
        ${isDark ? 'bg-gray-700/90' : 'bg-white/90'}
        ${isActive 
          ? `ring-2 ring-offset-2 ${isDark ? 'ring-white ring-offset-gray-800' : 'ring-gpt-green ring-offset-gray-50'}`
          : 'hover:ring-1 hover:ring-gpt-green/30'
        }
        backdrop-blur-sm
        shadow-[0_1px_1px_rgba(0,0,0,0.1),0_2px_2px_rgba(0,0,0,0.1),0_4px_4px_rgba(0,0,0,0.1),0_8px_8px_rgba(0,0,0,0.1)]
        hover:shadow-[0_1px_1px_rgba(0,0,0,0.15),0_2px_2px_rgba(0,0,0,0.15),0_4px_4px_rgba(0,0,0,0.15),0_8px_8px_rgba(0,0,0,0.15),0_16px_16px_rgba(0,0,0,0.15)]
      `}
      style={{
        '--category-color': `rgb(var(--${id}-color))`,
      } as React.CSSProperties}
    >
      <div className="flex flex-col items-center space-y-3">
        <motion.div
          variants={iconVariants}
          className="relative"
        >
          <Icon 
            size={24} 
            className={`transition-colors duration-300 ${isActive ? 'text-[rgb(var(--category-color))]' : ''}`}
          />
          {recentSearches > 0 && (
            <span className="absolute -top-2 -right-2 w-4 h-4 text-xs flex items-center justify-center bg-[rgb(var(--category-color))] text-white rounded-full">
              {recentSearches}
            </span>
          )}
        </motion.div>
        
        <span className="font-medium text-sm">{label}</span>
        
        <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
          {description}
        </p>

        <AnimatePresence>
          {isHovered && popularQueries.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10, rotateX: -10, translateZ: -10 }}
              animate={{ opacity: 1, y: 0, rotateX: 0, translateZ: 20 }}
              exit={{ opacity: 0, y: 10, rotateX: -10, translateZ: -10 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
              className={`
                absolute left-0 right-0 bottom-0 transform translate-y-full mt-2 p-2
                ${isDark ? 'bg-gray-800/95' : 'bg-white/95'}
                rounded-lg shadow-lg z-10 backdrop-blur-sm
              `}
            >
              <div className="text-xs font-medium mb-2">Popular Searches:</div>
              {popularQueries.map((query, i) => (
                <div
                  key={i}
                  className={`
                    text-xs py-1.5 px-3 rounded-lg transition-colors duration-200
                    ${isDark ? 'hover:bg-gray-700/80' : 'hover:bg-gray-100/80'}
                    cursor-pointer
                  `}
                >
                  {query}
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}