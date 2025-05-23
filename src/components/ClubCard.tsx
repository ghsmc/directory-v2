import React, { useState } from 'react';
import { ArrowUpRight, Mail, Users, Calendar, Tag, Star, ChevronDown, ChevronUp, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Club {
  id: string;
  name: string;
  logo: string;
  category: string;
  score: number;
  description: string;
  meetings: string;
  howToJoin: string;
  activityLevel: 'Very Active' | 'Active' | 'Moderately Active' | 'Less Active';
  contact: string;
  tags: string[];
}

interface ClubCardProps extends Club {
  isDark?: boolean;
}

export function ClubCard({
  name,
  logo,
  category,
  score,
  description,
  meetings,
  howToJoin,
  activityLevel,
  contact,
  tags,
  isDark = false,
}: ClubCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const activityLevelColor = {
    'Very Active': 'text-emerald-500',
    'Active': 'text-blue-500',
    'Moderately Active': 'text-yellow-500',
    'Less Active': 'text-gray-500'
  };

  const SectionHeader = ({ icon: Icon, children }: { icon: React.ElementType, children: React.ReactNode }) => (
    <div className={`
      flex items-center gap-2 mb-2 pb-2 border-b
      ${isDark ? 'border-white/10' : 'border-gray-200'}
    `}>
      <Icon 
        size={14} 
        className={isDark ? 'text-white/40' : 'text-gray-400'} 
      />
      <h4 className={`
        text-xs font-medium tracking-wider uppercase
        ${isDark ? 'text-white/40' : 'text-gray-500'}
      `}>
        {children}
      </h4>
    </div>
  );

  return (
    <div className={`
      p-4 border rounded-lg
      ${isDark ? 'border-white/10 hover:bg-white/[0.02]' : 'border-gray-200 hover:bg-gray-50'}
      transition-colors duration-200
    `}>
      <div className="flex items-start gap-4">
        <img 
          src={logo} 
          alt={name}
          className="w-12 h-12 rounded-lg object-cover bg-white flex-shrink-0"
        />
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h3 className={`
                  text-lg font-semibold
                  ${isDark ? 'text-white' : 'text-gray-900'}
                `}>
                  {name}
                </h3>
                <ArrowUpRight size={16} className={isDark ? 'text-white/40' : 'text-gray-400'} />
              </div>
              
              <div className="mt-1 flex items-center gap-3">
                <div className="flex items-center gap-1.5">
                  <div className={`
                    px-1.5 py-0.5 rounded font-mono text-white text-xs
                    ${score >= 90 ? 'bg-emerald-500' :
                      score >= 80 ? 'bg-emerald-500' :
                      score >= 70 ? 'bg-yellow-500' :
                      'bg-gray-500'}
                  `}>
                    {score}/100
                  </div>
                </div>
                <span className={`text-sm ${isDark ? 'text-white/60' : 'text-gray-600'}`}>
                  {category}
                </span>
              </div>
            </div>

            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className={`
                p-2 rounded-lg transition-colors duration-200
                ${isDark 
                  ? 'hover:bg-white/10 text-white/60' 
                  : 'hover:bg-gray-100 text-gray-500'
                }
              `}
            >
              {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            </button>
          </div>

          <p className={`
            mt-2 text-sm line-clamp-2
            ${isDark ? 'text-white/70' : 'text-gray-600'}
          `}>
            {description}
          </p>

          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className={`
                  mt-4 pt-4 border-t space-y-6
                  ${isDark ? 'border-white/10' : 'border-gray-200'}
                `}>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <SectionHeader icon={Calendar}>
                        Meetings
                      </SectionHeader>
                      <p className={`
                        text-sm
                        ${isDark ? 'text-white/70' : 'text-gray-600'}
                      `}>
                        {meetings}
                      </p>
                    </div>

                    <div>
                      <SectionHeader icon={Users}>
                        How to Join
                      </SectionHeader>
                      <p className={`
                        text-sm
                        ${isDark ? 'text-white/70' : 'text-gray-600'}
                      `}>
                        {howToJoin}
                      </p>
                    </div>
                  </div>

                  <div>
                    <SectionHeader icon={Info}>
                      Club Details
                    </SectionHeader>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className={isDark ? 'text-white/60' : 'text-gray-500'}>
                          Activity Level
                        </span>
                        <span className={activityLevelColor[activityLevel]}>
                          {activityLevel}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Mail size={14} className={isDark ? 'text-white/40' : 'text-gray-400'} />
                        <a 
                          href={`mailto:${contact}`}
                          className={`
                            text-sm
                            ${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-500'}
                          `}
                        >
                          {contact}
                        </a>
                      </div>
                    </div>
                  </div>

                  <div>
                    <SectionHeader icon={Tag}>
                      Tags
                    </SectionHeader>
                    <div className="flex flex-wrap gap-2">
                      {tags.map((tag) => (
                        <span
                          key={tag}
                          className={`
                            text-xs px-2 py-1 rounded-md
                            ${isDark 
                              ? 'bg-white/5 text-white/80' 
                              : 'bg-gray-100 text-gray-800'
                            }
                          `}
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}