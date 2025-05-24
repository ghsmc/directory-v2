import React, { useMemo, useState } from 'react';
import { Heart, Search, X } from 'lucide-react';
import { interests as ALL_INTERESTS } from '../../utils/auth/constants';

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
  /* ------------------------------------------------ State ------------------------------------------------ */
  const [query, setQuery] = useState('');
  const [searchFocused, setSearchFocused] = useState(false);

  /* --------------------------------------------- Derived data -------------------------------------------- */
  const filteredInterests = useMemo(() => {
    const q = query.trim().toLowerCase();
    return ALL_INTERESTS.filter((i) => i.toLowerCase().includes(q));
  }, [query]);

  // 8 quick‑pick ideas — placeholder for ML‑driven recs later
  const suggestions = useMemo(() => ALL_INTERESTS.slice(0, 8), []);

  /* ------------------------------------------------ Handlers --------------------------------------------- */
  const toggleInterest = (interest: string) => {
    const next = new Set(selectedInterests);
    next.has(interest) ? next.delete(interest) : next.add(interest);
    setSelectedInterests(next);
  };

  /* -------------------------------------------------- UI ------------------------------------------------- */
  return (
    <>
      {/* Title */}
      <label className="block text-sm font-medium text-gray-700 mb-3">
        <Heart size={16} className="inline mr-2" />
        {clarity === 'yes'
          ? 'What areas are you interested in?'
          : "Do you have an idea of any paths you're interested in?"}
      </label>

      {/* Search */}
      <div className="relative mb-4">
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

      {/* Selected chips */}
      {selectedInterests.size > 0 && (
        <div className="overflow-x-auto mb-4 pb-1">
          <div className="flex gap-2 min-w-max">
            {Array.from(selectedInterests).map((interest) => (
              <span
                key={interest}
                className="flex items-center bg-blue-100 text-blue-700 border border-blue-200 rounded-full text-sm font-medium px-3 py-1 whitespace-nowrap"
              >
                {interest}
                <button
                  type="button"
                  className="ml-1 hover:text-blue-900"
                  onClick={() => toggleInterest(interest)}
                >
                  <X size={12} />
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Suggestions grid (only before focus) */}
      {!searchFocused && query.trim() === '' && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            You might be interested in
          </h4>
          <div className="grid grid-cols-2 gap-2">
            {suggestions.map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => toggleInterest(s)}
                className={`px-3 py-2 rounded-lg text-sm font-medium text-left transition-colors ${
                  selectedInterests.has(s)
                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Full grid (after focus) */}
      {searchFocused && (
        <div className="max-h-56 overflow-y-auto pr-1">
          <div className="grid grid-cols-2 gap-2">
            {(query.trim() === '' ? ALL_INTERESTS : filteredInterests).map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => toggleInterest(interest)}
                className={`px-3 py-2 rounded-lg text-sm font-medium text-left transition-colors ${
                  selectedInterests.has(interest)
                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
