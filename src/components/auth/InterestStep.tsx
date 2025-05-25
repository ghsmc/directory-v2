import React, { useMemo, useState } from 'react';
import { Heart, Search, X } from 'lucide-react';
import { interests } from '../../utils/auth/constants';
import { getInterestIcon } from '../../utils/auth/icons';

interface InterestStepProps {
  selectedInterests: Set<string>;
  setSelectedInterests: (interests: Set<string>) => void;
  clarity: 'yes' | 'no' | null;
  onFieldFocus?: (field: string) => void;
}

export function InterestStep({
  selectedInterests,
  setSelectedInterests,
  clarity,
  onFieldFocus
}: InterestStepProps) {
  const [query, setQuery] = useState('');
  const [searchFocused, setSearchFocused] = useState(false);

  const filteredInterests = useMemo(() => {
    const q = query.trim().toLowerCase();
    return interests.filter((i) => i.toLowerCase().includes(q));
  }, [query]);

  const suggestions = useMemo(() => interests.slice(0, 12), []);

  const toggleInterest = (interest: string) => {
    const next = new Set(selectedInterests);
    next.has(interest) ? next.delete(interest) : next.add(interest);
    setSelectedInterests(next);
  };

  const renderInterestGrid = (interestsToShow: string[]) => (
    <div className="grid grid-cols-3 sm:grid-cols-4 gap-3">
      {interestsToShow.map((interest) => {
        const Icon = getInterestIcon(interest);
        return (
          <button
            key={interest}
            type="button"
            onClick={() => toggleInterest(interest)}
            className={`
              relative group flex flex-col items-center gap-2 p-4 rounded-xl border transition-all duration-200
              ${selectedInterests.has(interest)
                ? 'bg-purple-50 border-purple-200 shadow-sm'
                : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-sm'
              }
            `}
          >
            <div className="relative w-16 h-16 rounded-xl bg-white border border-gray-100 flex items-center justify-center">
              <Icon 
                size={32} 
                className={selectedInterests.has(interest) ? 'text-purple-500' : 'text-gray-600'} 
              />
              {selectedInterests.has(interest) && (
                <div className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-purple-500 rounded-full flex items-center justify-center">
                  <X size={12} className="text-white" />
                </div>
              )}
            </div>
            <span className="text-xs font-medium text-center line-clamp-2 text-gray-900">
              {interest}
            </span>
          </button>
        )
      })}
    </div>
  );

  return (
    <>
      <label className="block text-sm font-medium text-gray-700 mb-3">
        <Heart size={16} className="inline mr-2" />
        {clarity === 'yes'
          ? 'What areas are you interested in?'
          : "Do you have an idea of any paths you're interested in?"}
      </label>

      <div className="relative mb-6">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        />
        <input
          type="text"
          placeholder="Search interests..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          onFocus={() => {
            setSearchFocused(true);
            onFieldFocus && onFieldFocus('interests');
          }}
          onBlur={() => setSearchFocused(false)}
        />
      </div>

      {selectedInterests.size > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Selected Interests</h4>
          {renderInterestGrid(Array.from(selectedInterests))}
        </div>
      )}

      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-3">
          {query.trim() ? 'Search Results' : 'Popular Interests'}
        </h4>
        {renderInterestGrid(query.trim() ? filteredInterests : suggestions)}
      </div>
    </>
  );
}