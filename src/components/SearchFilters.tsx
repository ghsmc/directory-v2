import React, { useState } from 'react';
import { Search, MapPin, Building2, Briefcase, Code2, Users2, DollarSign, GraduationCap, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';

interface SearchFiltersProps {
  isDark: boolean;
}

const SectionTitle = ({ icon: Icon, children }: { icon: React.ElementType, children: React.ReactNode }) => (
  <div className="flex items-center gap-2 mb-3">
    <Icon size={16} style={{ color: 'var(--theme-sub)' }} />
    <h3 className="text-[11px] uppercase tracking-wide font-medium" style={{ color: 'var(--theme-sub)' }}>
      {children}
    </h3>
  </div>
);

const ShowMoreButton = ({ 
  isExpanded, 
  onClick, 
  count 
}: { 
  isExpanded: boolean;
  onClick: () => void;
  count: number;
}) => (
  <button
    onClick={onClick}
    className="flex items-center gap-1 text-xs font-medium mt-2 hover:opacity-80 transition-opacity"
    style={{ color: 'var(--theme-main)' }}
  >
    {isExpanded ? (
      <>
        Show Less
        <ChevronDown size={14} />
      </>
    ) : (
      <>
        Show {count} More
        <ChevronDown size={14} />
      </>
    )}
  </button>
);

export default function SearchFilters({ isDark }: SearchFiltersProps) {
  const [showMoreLocations, setShowMoreLocations] = useState(false);
  const [showMoreSectors, setShowMoreSectors] = useState(false);
  const [showMoreSkills, setShowMoreSkills] = useState(false);
  const [showMoreUniversities, setShowMoreUniversities] = useState(false);
  const [showMoreMajors, setShowMoreMajors] = useState(false);
  const [showMoreLevels, setShowMoreLevels] = useState(false);
  const [globalSearch, setGlobalSearch] = useState('');

  const filterByGlobalSearch = (items: any[], key: string = 'label') => {
    if (!globalSearch) return items;
    return items.filter(item => 
      item[key].toLowerCase().includes(globalSearch.toLowerCase())
    );
  };

  return (
    <div 
      className="w-64 h-screen overflow-y-auto hide-scrollbar px-4 py-4"
      style={{ 
        backgroundColor: 'var(--theme-bg)',
        borderRight: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
        color: 'var(--theme-text)'
      }}
    >
      {/* Global Search Input */}
      <div className="mb-6">
        <div 
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
          style={{ backgroundColor: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' }}
        >
          <Search size={14} style={{ color: 'var(--theme-sub)' }} />
          <input
            type="text"
            value={globalSearch}
            onChange={(e) => setGlobalSearch(e.target.value)}
            placeholder="Filter by keyword..."
            className="w-full bg-transparent border-none outline-none text-sm"
            style={{ 
              color: 'var(--theme-text)',
              '::placeholder': { color: 'var(--theme-sub)' }
            }}
          />
        </div>
      </div>

      {/* Location */}
      <div className="mb-6">
        <SectionTitle icon={MapPin}>LOCATION</SectionTitle>
        <div className="space-y-2">
          {filterByGlobalSearch([
            { label: 'Remote', count: '34,500', flag: '🌍' },
            { label: 'New York City', count: '23,712', flag: '🇺🇸' },
            { label: 'San Francisco', count: '21,134', flag: '🇺🇸' },
            { label: 'London', count: '16,802', flag: '🇬🇧' }
          ]).map(({ label, count, flag }) => (
            <label key={label} className="flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="form-checkbox rounded" />
                <span className="text-sm mr-1">{flag}</span>
                <span className="text-sm" style={{ color: 'var(--theme-text)' }}>
                  {label}
                </span>
              </div>
              <span className="text-xs" style={{ color: 'var(--theme-sub)' }}>
                {count}
              </span>
            </label>
          ))}
        </div>
        <ShowMoreButton 
          isExpanded={showMoreLocations}
          onClick={() => setShowMoreLocations(!showMoreLocations)}
          count={16}
        />
      </div>

      {/* Level */}
      <div className="mb-6">
        <SectionTitle icon={Users2}>LEVEL</SectionTitle>
        <div className="space-y-2">
          {[
            { label: 'Internship', count: '15,961' },
            { label: 'Entry Level', count: '78,840' },
            { label: 'Mid Level', count: '70,027' }
          ].map(({ label, count }) => (
            <label key={label} className="flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="form-checkbox rounded" />
                <span className="text-sm" style={{ color: 'var(--theme-text)' }}>
                  {label}
                </span>
              </div>
              <span className="text-xs" style={{ color: 'var(--theme-sub)' }}>
                {count}
              </span>
            </label>
          ))}
        </div>
        <ShowMoreButton 
          isExpanded={showMoreLevels}
          onClick={() => setShowMoreLevels(!showMoreLevels)}
          count={2}
        />
      </div>

      {/* Company Stage */}
      <div className="mb-6">
        <SectionTitle icon={Briefcase}>COMPANY STAGE</SectionTitle>
        <div className="space-y-2">
          {filterByGlobalSearch([
            { label: '🌱 Early-Stage Startup', count: '14,956' },
            { label: '🚀 Growth Stage', count: '23,825' },
            { label: '🦄 Unicorn', count: '43,825' },
            { label: '📈 Pre-IPO', count: '12,567' },
            { label: '💼 Public Company', count: '89,234' },
            { label: '🏛️ Established Institution', count: '67,453' }
          ]).map(({ label, count }) => (
            <label key={label} className="flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="form-checkbox rounded" />
                <span className="text-sm" style={{ color: 'var(--theme-text)' }}>
                  {label}
                </span>
              </div>
              <span className="text-xs" style={{ color: 'var(--theme-sub)' }}>
                {count}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Company Valuation */}
      <div className="mb-6">
        <SectionTitle icon={DollarSign}>COMPANY VALUATION</SectionTitle>
        <div className="space-y-2">
          {filterByGlobalSearch([
            { label: '<$1B', count: '45,311' },
            { label: '$1B - $5B', count: '38,604' },
            { label: '$5B - $30B', count: '22,336' },
            { label: '$30B - $100B', count: '15,576' },
            { label: '>$100B', count: '12,576' }
          ]).map(({ label, count }) => (
            <label key={label} className="flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="form-checkbox rounded" />
                <span className="text-sm" style={{ color: 'var(--theme-text)' }}>
                  {label}
                </span>
              </div>
              <span className="text-xs" style={{ color: 'var(--theme-sub)' }}>
                {count}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Skills */}
      <div className="mb-6">
        <SectionTitle icon={Code2}>SKILLS</SectionTitle>
        <div className="space-y-2">
          {filterByGlobalSearch([
            { label: 'Python', count: '45,678' },
            { label: 'JavaScript', count: '42,345' },
            { label: 'Machine Learning', count: '38,765' },
            { label: 'Data Analysis', count: '35,465' },
            { label: 'SQL', count: '32,456' },
            { label: 'Cloud Platforms', count: '30,123' },
            { label: 'React', count: '28,765' },
            { label: 'DevOps', count: '25,678' }
          ]).slice(0, showMoreSkills ? undefined : 8).map(({ label, count }) => (
            <label key={label} className="flex items-center justify-between group cursor-pointer">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="form-checkbox rounded" />
                <span className="text-sm" style={{ color: 'var(--theme-text)' }}>
                  {label}
                </span>
              </div>
              <span className="text-xs" style={{ color: 'var(--theme-sub)' }}>
                {count}
              </span>
            </label>
          ))}
        </div>
        <ShowMoreButton 
          isExpanded={showMoreSkills}
          onClick={() => setShowMoreSkills(!showMoreSkills)}
          count={12}
        />
      </div>
    </div>
  );
}

export { SearchFilters }