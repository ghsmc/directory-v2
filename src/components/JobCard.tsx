import React, { useState } from 'react';
import { ArrowUpRight, ChevronDown, ChevronUp, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface JobCardProps {
  companyLogo: string;
  companyName: string;
  jobTitle: string;
  description: string;
  location: string;
  salary?: string;
  postedDate: string;
  skills: string[];
  metrics: {
    trajectory: number;
    valuation?: string;
    funding?: string;
    lastRaised?: string;
    age?: string;
    employees: string;
    openJobs: number;
  };
  badges: {
    unicorn?: boolean;
    trueUpRemote200?: boolean;
  };
  isDark?: boolean;
  type?: 'job' | 'club' | 'lab' | 'course';
}

export function JobCard({
  companyLogo,
  companyName,
  jobTitle,
  description,
  location,
  salary,
  postedDate,
  skills,
  metrics,
  badges,
  isDark = false,
  type = 'job'
}: JobCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isApplied, setIsApplied] = useState(false);

  const getActionButtonText = () => {
    if (isApplied) return 'Applied';
    switch (type) {
      case 'club':
        return 'Join';
      default:
        return 'Apply';
    }
  };

  return (
    <div 
      className="p-4 border rounded-lg transition-colors duration-200 w-full"
      style={{ 
        backgroundColor: 'var(--theme-bg)',
        borderColor: 'var(--theme-border)',
        color: 'var(--theme-text)'
      }}
    >
      <div className="flex items-start gap-3 min-w-0">
        <img 
          src={companyLogo} 
          alt={companyName}
          className="w-8 h-8 rounded object-contain bg-white flex-shrink-0"
        />
        
        <div className="flex-1 min-w-0 overflow-hidden">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0 flex-1">
              <h3 className="text-[14px] font-semibold flex items-center gap-2 truncate" style={{ color: 'var(--theme-text)' }}>
                {jobTitle}
                <ArrowUpRight size={14} style={{ color: 'var(--theme-sub)' }} className="flex-shrink-0" />
              </h3>
              
              <div className="mt-0.5 flex items-center gap-2 min-w-0">
                <span className="text-[13px] font-medium whitespace-nowrap" style={{ color: 'var(--theme-text)' }}>
                  {companyName}
                </span>
                <span style={{ color: 'var(--theme-sub)' }}>•</span>
                <span className="text-sm truncate" style={{ color: 'var(--theme-sub)' }}>
                  {description}
                </span>
              </div>
            </div>

            <div className="flex flex-col items-end flex-shrink-0">
              <div className="text-[11px] uppercase tracking-wide font-medium text-right whitespace-nowrap" style={{ color: 'var(--theme-sub)' }}>
                {location}
              </div>
              <div className="text-[11px] mt-0.5" style={{ color: 'var(--theme-sub)' }}>
                {postedDate}
              </div>
            </div>
          </div>

          {salary && (
            <div className="mt-2 text-sm font-medium" style={{ color: 'var(--theme-text)' }}>
              {salary}
            </div>
          )}

          {skills.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {skills.map((skill) => (
                <span
                  key={skill}
                  className="text-[11px] font-medium px-1.5 py-0.5 rounded"
                  style={{ 
                    backgroundColor: isDark ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.05)',
                    color: 'var(--theme-text)'
                  }}
                >
                  {skill}
                </span>
              ))}
            </div>
          )}

          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center gap-3 flex-wrap text-[12px]">
              {metrics.trajectory && (
                <div className="flex items-center gap-1.5">
                  <div className={`
                    px-1.5 py-0.5 rounded font-mono text-white text-xs
                    ${metrics.trajectory >= 80 ? 'bg-emerald-500' :
                      metrics.trajectory >= 70 ? 'bg-yellow-500' :
                      'bg-gray-500'}
                  `}>
                    {metrics.trajectory}
                  </div>
                  <span style={{ color: 'var(--theme-sub)' }}>
                    Match Score
                  </span>
                </div>
              )}

              {badges.unicorn && (
                <div className="flex items-center gap-1">
                  <span role="img" aria-label="unicorn">🦄</span>
                  <span style={{ color: 'var(--theme-sub)' }}>Unicorn</span>
                </div>
              )}

              {metrics.valuation && (
                <div className="hidden md:flex items-center gap-1">
                  <span className="font-semibold" style={{ color: 'var(--theme-text)' }}>
                    {metrics.valuation}
                  </span>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsApplied(true)}
                className={`
                  relative px-3 py-1 rounded-lg text-[11px] font-medium transition-all duration-200
                  ${isApplied
                    ? 'bg-emerald-100 text-emerald-600'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                  }
                `}
              >
                <motion.span
                  initial={false}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-1"
                >
                  {isApplied && <Check size={12} />}
                  {getActionButtonText()}
                </motion.span>
              </button>

              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-1 rounded-lg transition-colors duration-200 flex-shrink-0"
                style={{ 
                  color: 'var(--theme-sub)',
                  '&:hover': {
                    backgroundColor: 'var(--theme-hover)'
                  }
                }}
              >
                {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}