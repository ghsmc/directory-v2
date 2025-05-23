import React from 'react';
import { ClubCard } from './ClubCard';
import { Star } from 'lucide-react';

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

interface ClubListProps {
  clubs: Club[];
  isDark?: boolean;
}

export function ClubList({ clubs, isDark = false }: ClubListProps) {
  return (
    <div className="space-y-2 max-w-full">
      {clubs.map((club) => (
        <div 
          key={club.id}
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
          
          <ClubCard {...club} isDark={isDark} />
        </div>
      ))}
    </div>
  );
}