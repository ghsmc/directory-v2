import React from 'react';
import { JobCard } from './JobCard';
import { Star } from 'lucide-react';

interface Job {
  id: string;
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
}

interface JobListProps {
  jobs: Job[];
  isDark?: boolean;
}

export function JobList({ jobs, isDark = false }: JobListProps) {
  return (
    <div className="space-y-2 max-w-full">
      {jobs.map((job) => (
        <div 
          key={job.id}
          className={`
            group relative overflow-hidden transition-all duration-200
            ${isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-gray-50'}
          `}
        >
          <button 
            className={`
              absolute top-4 right-4 p-2 rounded-lg opacity-0 group-hover:opacity-100
              transition-all duration-200 z-10
              ${isDark 
                ? 'hover:bg-white/10 text-white/60 hover:text-white/90' 
                : 'hover:bg-gray-100 text-gray-400 hover:text-gray-600'
              }
            `}
          >
            <Star size={20} />
          </button>
          
          <JobCard {...job} isDark={isDark} />
        </div>
      ))}
    </div>
  );
}