import React, { useMemo, useState } from 'react';
import { Briefcase, Search, X } from 'lucide-react';
import { companies as ALL_COMPANIES } from '../../utils/auth/constants';

interface CompanyStepProps {
  selectedCompanies: Set<string>;
  setSelectedCompanies: (companies: Set<string>) => void;
  clarity: 'yes' | 'no' | null;
  onFieldFocus?: (field: string) => void;
}

export function CompanyStep({
  selectedCompanies,
  setSelectedCompanies,
  clarity,
  onFieldFocus
}: CompanyStepProps) {
  // State for search query
  const [query, setQuery] = useState('');
  const [searchFocused, setSearchFocused] = useState(false);

  // Filtered companies based on search
  const filteredCompanies = useMemo(() => {
    const q = query.trim().toLowerCase();
    return ALL_COMPANIES.filter((c) => c.toLowerCase().includes(q));
  }, [query]);

  // Suggestions: first 8 companies
  const suggestions = useMemo(() => ALL_COMPANIES.slice(0, 8), []);

  // Toggle company selection
  const toggleCompany = (company: string) => {
    const next = new Set(selectedCompanies);
    next.has(company) ? next.delete(company) : next.add(company);
    setSelectedCompanies(next);
  };

  return (
    <>
      {/* Title */}
      <label className="block text-sm font-medium text-gray-700 mb-3">
        <Briefcase size={16} className="inline mr-2" />
        {clarity === 'yes'
          ? 'What companies are you interested in?'
          : "Are there any companies you find inspiring or interesting?"}
      </label>

      {/* Search */}
      <div className="relative mb-4">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        />
        <input
          type="text"
          placeholder="Search companies..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          onFocus={() => {
            setSearchFocused(true);
            onFieldFocus && onFieldFocus('companies');
          }}
          onBlur={() => setSearchFocused(false)}
        />
      </div>

      {/* Selected chips */}
      {selectedCompanies.size > 0 && (
        <div className="overflow-x-auto mb-4 pb-1">
          <div className="flex gap-2 min-w-max">
            {Array.from(selectedCompanies).map((company) => (
              <span
                key={company}
                className="flex items-center bg-blue-100 text-blue-700 border border-blue-200 rounded-full text-sm font-medium px-3 py-1 whitespace-nowrap"
              >
                {company}
                <button
                  type="button"
                  className="ml-1 hover:text-blue-900"
                  onClick={() => toggleCompany(company)}
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
                onClick={() => toggleCompany(s)}
                className={`px-3 py-2 rounded-lg text-sm font-medium text-left transition-colors ${
                  selectedCompanies.has(s)
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
            {(query.trim() === '' ? ALL_COMPANIES : filteredCompanies).map((company) => (
              <button
                key={company}
                type="button"
                onMouseDown={e => { e.preventDefault(); toggleCompany(company); }}
                className={`px-3 py-2 rounded-lg text-sm font-medium text-left transition-colors ${
                  selectedCompanies.has(company)
                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {company}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Helper text */}
      <p className="text-xs text-gray-500 mt-2">
        We'll use this to surface mentors, alumni paths, and open roles.
      </p>
    </>
  );
} 