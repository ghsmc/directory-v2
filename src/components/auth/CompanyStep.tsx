import React, { useMemo, useState } from 'react';
import { Briefcase, Search, X } from 'lucide-react';
import { companies } from '../../utils/auth/constants';

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
  const [query, setQuery] = useState('');
  const [searchFocused, setSearchFocused] = useState(false);

  const filteredCompanies = useMemo(() => {
    const q = query.trim().toLowerCase();
    return companies.filter((c) => c.name.toLowerCase().includes(q));
  }, [query]);

  const suggestions = useMemo(() => companies.slice(0, 12), []);

  const toggleCompany = (companyName: string) => {
    const next = new Set(selectedCompanies);
    next.has(companyName) ? next.delete(companyName) : next.add(companyName);
    setSelectedCompanies(next);
  };

  const renderCompanyGrid = (companiesToShow: typeof companies) => (
    <div className="grid grid-cols-3 sm:grid-cols-4 gap-3">
      {companiesToShow.map((company) => (
        <button
          key={company.name}
          type="button"
          onClick={() => toggleCompany(company.name)}
          className={`
            relative group flex flex-col items-center gap-2 p-4 rounded-xl border transition-all duration-200
            ${selectedCompanies.has(company.name)
              ? 'bg-blue-50 border-blue-200 shadow-sm'
              : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-sm'
            }
          `}
        >
          <div className="relative w-16 h-16 rounded-xl bg-white border border-gray-100 p-2 flex items-center justify-center">
            <img
              src={`https://img.logo.dev/${company.domain}?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ`}
              alt={company.name}
              className="w-12 h-12 object-contain"
            />
            {selectedCompanies.has(company.name) && (
              <div className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                <X size={12} className="text-white" />
              </div>
            )}
          </div>
          <span className="text-xs font-medium text-center line-clamp-2 text-gray-900">
            {company.name}
          </span>
        </button>
      ))}
    </div>
  );

  return (
    <>
      <label className="block text-sm font-medium text-gray-700 mb-3">
        <Briefcase size={16} className="inline mr-2" />
        {clarity === 'yes'
          ? 'What companies are you interested in?'
          : "Are there any companies you find inspiring or interesting?"}
      </label>

      <div className="relative mb-6">
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

      {selectedCompanies.size > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Selected Companies</h4>
          {renderCompanyGrid(companies.filter(c => selectedCompanies.has(c.name)))}
        </div>
      )}

      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-3">
          {query.trim() ? 'Search Results' : 'Popular Companies'}
        </h4>
        {renderCompanyGrid(query.trim() ? filteredCompanies : suggestions)}
      </div>

      <p className="text-xs text-gray-500 mt-4">
        We'll use this to surface mentors, alumni paths, and open roles.
      </p>
    </>
  );
}