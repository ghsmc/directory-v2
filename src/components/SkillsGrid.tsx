import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Star } from 'lucide-react';

interface Skill {
  name: string;
  level: number;
  trend: 'up' | 'down' | 'stable';
  demand: number;
  growth: string;
}

interface SkillsGridProps {
  skills: Skill[];
  isDark: boolean;
}

export function SkillsGrid({ skills, isDark }: SkillsGridProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {skills.map((skill) => (
        <motion.div
          key={skill.name}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className={`
            relative p-4 rounded-lg overflow-hidden
            ${isDark ? 'bg-gray-800' : 'bg-white'}
            border ${isDark ? 'border-gray-700' : 'border-gray-200'}
          `}
        >
          <div className="relative z-10">
            <div className="flex items-start justify-between">
              <div>
                <h3 className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {skill.name}
                </h3>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        size={12}
                        className={`
                          ${i < Math.floor(skill.level / 20)
                            ? 'text-amber-400 fill-amber-400'
                            : isDark
                              ? 'text-gray-700'
                              : 'text-gray-200'
                          }
                        `}
                      />
                    ))}
                  </div>
                </div>
              </div>
              <div className={`
                flex items-center gap-1 text-xs font-medium
                ${skill.trend === 'up' ? 'text-emerald-500' : 'text-red-500'}
              `}>
                <TrendingUp size={14} />
                {skill.growth}
              </div>
            </div>
            
            <div className="mt-3">
              <div className="flex items-center justify-between text-xs mb-1">
                <span className={isDark ? 'text-gray-400' : 'text-gray-500'}>
                  Market Demand
                </span>
                <span className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {skill.demand}%
                </span>
              </div>
              <div className="h-1.5 rounded-full bg-gray-200 overflow-hidden">
                <div 
                  className="h-full rounded-full bg-blue-500"
                  style={{ width: `${skill.demand}%` }}
                />
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}