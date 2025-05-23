import React, { useState } from 'react';
import { Search, Send } from 'lucide-react';

interface Company {
  id: string;
  name: string;
  logo: string;
  description: string;
  industry: string;
  matchScore?: number;
  valuation?: string;
  status?: string;
  jobCount: number;
}

interface CompaniesSectionProps {
  isDark: boolean;
  following: Company[];
  recommended: Company[];
}

export function CompaniesSection({ isDark, following, recommended }: CompaniesSectionProps) {
  const [followingSearch, setFollowingSearch] = useState('');
  const [recommendedSearch, setRecommendedSearch] = useState('');
  const [followedCompanies, setFollowedCompanies] = useState<Set<string>>(new Set());
  const [visibleCount, setVisibleCount] = useState(8);

  const filterCompanies = (companies: Company[], search: string) => {
    if (!search) return companies;
    const searchLower = search.toLowerCase();
    return companies.filter(company => 
      company.name.toLowerCase().includes(searchLower) ||
      company.description.toLowerCase().includes(searchLower)
    );
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'bg-emerald-500 text-white';
    if (score >= 85) return 'bg-green-500 text-white';
    if (score >= 80) return 'bg-lime-500 text-white';
    if (score >= 75) return 'bg-yellow-500 text-white';
    if (score >= 70) return 'bg-orange-500 text-white';
    return 'bg-red-500 text-white';
  };

  const toggleFollow = (companyId: string) => {
    setFollowedCompanies(prev => {
      const next = new Set(prev);
      if (next.has(companyId)) {
        next.delete(companyId);
      } else {
        next.add(companyId);
      }
      return next;
    });
  };

  const renderSearchBar = (
    placeholder: string,
    value: string,
    onChange: (value: string) => void
  ) => (
    <div className={`
      flex items-center gap-2 px-3 py-2 rounded-lg mb-4
      ${isDark ? 'bg-gray-700/50' : 'bg-gray-50'}
    `}>
      <Search size={14} className={isDark ? 'text-gray-400' : 'text-gray-500'} />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`
          w-full bg-transparent border-none outline-none text-sm
          ${isDark
            ? 'text-white placeholder:text-gray-400'
            : 'text-gray-900 placeholder:text-gray-500'
          }
        `}
      />
    </div>
  );

  const renderColumnHeaders = () => (
    <div className="flex items-center gap-4 px-2 py-2 text-[11px] uppercase tracking-wider font-medium text-gray-500">
      <div className="w-[70px]"></div>
      <div className="w-[30px] font-bold text-black">Rank</div>
      <div className="w-[30px]"></div>
      <div className="flex-1">Company</div>
      <div className="w-[200px]">Description</div>
      <div className="w-[100px] text-center">Match</div>
      <div className="w-[120px]">Industry</div>
      <div className="w-[100px] text-right">Valuation</div>
    </div>
  );

  const renderCompanyList = (companies: Company[], searchValue: string) => (
    <div className="space-y-[1px]">
      {renderColumnHeaders()}
      {filterCompanies(companies, searchValue).map((company, index) => {
        const paddedIndex = (index + 1).toString().padStart(2, '0');
        const isFollowing = followedCompanies.has(company.id);
        
        return (
          <div
            key={company.id}
            className={`
              flex items-center gap-4 py-3 px-2 transition-colors group
              ${isDark 
                ? 'hover:bg-gray-700/50' 
                : 'hover:bg-gray-50'
              }
            `}
          >
            <button
              onClick={() => toggleFollow(company.id)}
              className={`
                w-[70px] px-2.5 py-1 text-[11px] font-medium rounded transition-colors
                ${isFollowing
                  ? isDark
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'bg-blue-50 text-blue-600'
                  : isDark
                    ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }
              `}
            >
              {isFollowing ? 'Following' : 'Follow'}
            </button>

            <div className="w-[30px] text-[13px] font-bold text-black text-center">
              {paddedIndex}
            </div>

            <div className="w-[30px] h-6 flex-shrink-0">
              <img 
                src={company.logo} 
                alt={company.name}
                className="w-6 h-6 rounded object-contain bg-white"
              />
            </div>

            <div className="flex-1 min-w-0">
              <div className="text-[13px] font-medium" style={{ color: 'var(--theme-text)' }}>
                {company.name}
              </div>
            </div>

            <div className="w-[200px]">
              <div className="text-[13px]" style={{ color: 'var(--theme-sub)' }}>
                {company.description}
              </div>
            </div>

            {company.matchScore && (
              <div className="w-[100px] text-center">
                <div className={`
                  inline-block px-2 py-0.5 rounded text-[12px] font-medium
                  ${getMatchScoreColor(company.matchScore)}
                `}>
                  {company.matchScore}
                </div>
              </div>
            )}

            <div className="w-[120px]">
              <div className={`
                inline-block px-2 py-0.5 rounded-full text-[11px]
                ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
              `}>
                {company.industry}
              </div>
            </div>

            <div className="w-[100px] text-right">
              <div className="text-[13px] font-medium" style={{ color: 'var(--theme-text)' }}>
                {company.valuation}
              </div>
              <div className="text-[12px]" style={{ color: 'var(--theme-sub)' }}>
                {company.status}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );

  const allCompanies = [
    {
      id: '1',
      name: 'xAI',
      logo: 'https://img.logo.dev/xai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Artificial intelligence research',
      industry: 'AI Research',
      matchScore: 95,
      valuation: '$45.0B',
      status: 'Private',
      jobCount: 156
    },
    {
      id: '2',
      name: 'Anthropic',
      logo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI systems and safety',
      industry: 'AI Safety',
      matchScore: 92,
      valuation: '$61.5B',
      status: 'Private',
      jobCount: 45
    },
    {
      id: '3',
      name: 'Perplexity AI',
      logo: 'https://img.logo.dev/perplexity.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Conversational AI platform',
      industry: 'AI Search',
      matchScore: 88,
      valuation: '$9.0B',
      status: 'Private',
      jobCount: 28
    },
    {
      id: '4',
      name: 'Mistral AI',
      logo: 'https://img.logo.dev/mistral.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Generative AI models',
      industry: 'AI/ML',
      matchScore: 86,
      valuation: '$6.2B',
      status: 'Private',
      jobCount: 42
    },
    {
      id: '5',
      name: 'Figure AI',
      logo: 'https://img.logo.dev/figure.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Humanoid robotics',
      industry: 'Robotics',
      matchScore: 84,
      valuation: '$2.7B',
      status: 'Private',
      jobCount: 89
    },
    {
      id: '6',
      name: 'Safe Superintelligence',
      logo: 'https://img.logo.dev/ssi.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Safe artificial intelligence',
      industry: 'AI Safety',
      matchScore: 82,
      valuation: '$5.0B',
      status: 'Private',
      jobCount: 34
    },
    {
      id: '7',
      name: 'Sierra',
      logo: 'https://img.logo.dev/sierra.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Enterprise AI',
      industry: 'AI/ML',
      matchScore: 80,
      valuation: '$4.5B',
      status: 'Private',
      jobCount: 67
    },
    {
      id: '8',
      name: 'The Bot Company',
      logo: 'https://img.logo.dev/thebotcompany.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Household robots',
      industry: 'Robotics',
      matchScore: 78,
      valuation: '$2.0B',
      status: 'Private',
      jobCount: 45
    },
    {
      id: '9',
      name: 'Cohere',
      logo: 'https://img.logo.dev/cohere.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Enterprise LLMs',
      industry: 'AI/ML',
      matchScore: 76,
      valuation: '$2.2B',
      status: 'Private',
      jobCount: 38
    },
    {
      id: '10',
      name: 'Inflection AI',
      logo: 'https://img.logo.dev/inflection.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Personal AI assistants',
      industry: 'AI/ML',
      matchScore: 75,
      valuation: '$4.0B',
      status: 'Private',
      jobCount: 42
    },
    {
      id: '11',
      name: 'Scale AI',
      logo: 'https://img.logo.dev/scale.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI infrastructure',
      industry: 'AI/ML',
      matchScore: 74,
      valuation: '$7.3B',
      status: 'Private',
      jobCount: 89
    },
    {
      id: '12',
      name: 'Adept AI',
      logo: 'https://img.logo.dev/adept.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI agents and automation',
      industry: 'AI/ML',
      matchScore: 73,
      valuation: '$1.0B',
      status: 'Private',
      jobCount: 28
    },
    {
      id: '13',
      name: 'Character AI',
      logo: 'https://img.logo.dev/character.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI characters and chat',
      industry: 'AI/ML',
      matchScore: 72,
      valuation: '$1.0B',
      status: 'Private',
      jobCount: 34
    }
  ];

  const filteredCompanies = filterCompanies(allCompanies, followingSearch);
  const hasMore = visibleCount < filteredCompanies.length;

  return (
    <div className="flex gap-6">
      <div className="w-3/4">
        <div className={`
          rounded-xl border overflow-hidden h-[calc(100vh-12rem)]
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="h-full flex flex-col">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    Companies
                  </h2>
                  <p className={`text-sm mt-1 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                    Track and discover companies
                  </p>
                </div>
              </div>

              {renderSearchBar(
                "Search companies...",
                followingSearch,
                setFollowingSearch
              )}
            </div>

            <div className="flex-1 overflow-auto">
              <div className="px-6">
                {renderCompanyList(filteredCompanies.slice(0, visibleCount), followingSearch)}
              </div>
            </div>

            {hasMore && (
              <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={() => setVisibleCount(prev => prev + 5)}
                  className={`
                    w-full py-2 rounded-lg text-sm font-medium transition-colors
                    ${isDark
                      ? 'bg-gray-700 hover:bg-gray-600 text-white'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                    }
                  `}
                >
                  Load More Companies
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="w-1/4">
        <div className={`
          rounded-xl border overflow-hidden sticky top-4 h-[calc(100vh-12rem)]
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="h-full p-4 overflow-auto">
            <div className="flex items-center gap-2 mb-4">
              <img 
                src="https://gmccain.com/milo.png"
                alt="Milo"
                className="w-6 h-6 rounded-lg"
              />
              <h3 className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Milo's Analysis
              </h3>
            </div>

            <div className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
              <p className="mb-4">
                Based on your ML and Python expertise, I've identified several promising AI companies that align with your skills. xAI and Anthropic stand out with their focus on advanced AI research and competitive compensation packages.
              </p>

              <div className="space-y-4">
                <div>
                  <div className={`text-xs font-medium mb-2 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                    Top Matches
                  </div>
                  <div className="space-y-2">
                    {filteredCompanies.slice(0, 3).map(company => (
                      <div key={company.id} className={`
                        p-2 rounded-lg
                        ${isDark ? 'bg-gray-700' : 'bg-gray-50'}
                      `}>
                        <div className="flex items-center gap-2">
                          <img 
                            src={company.logo}
                            alt={company.name}
                            className="w-4 h-4 rounded bg-white"
                          />
                          <span className="text-sm font-medium">{company.name}</span>
                          <span className={`
                            text-xs px-1.5 py-0.5 rounded
                            ${getMatchScoreColor(company.matchScore || 0)}
                          `}>
                            {company.matchScore}
                          </span>
                        </div>
                        <p className="text-xs mt-1 opacity-80">{company.description}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div className={`text-xs font-medium mb-2 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                    Industry Insights
                  </div>
                  <div className="space-y-2">
                    <div className={`
                      p-2 rounded-lg
                      ${isDark ? 'bg-gray-700' : 'bg-gray-50'}
                    `}>
                      <div className="text-xs font-medium mb-1">AI Safety Focus</div>
                      <p className="text-xs opacity-80">
                        Companies like Anthropic are prioritizing AI safety research, offering opportunities to work on cutting-edge alignment challenges.
                      </p>
                    </div>
                    <div className={`
                      p-2 rounded-lg
                      ${isDark ? 'bg-gray-700' : 'bg-gray-50'}
                    `}>
                      <div className="text-xs font-medium mb-1">Competitive Packages</div>
                      <p className="text-xs opacity-80">
                        AI research positions are offering premium compensation, with average packages ranging from $180K to $250K.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className={`
                flex items-center gap-2 p-2 rounded-lg
                ${isDark ? 'bg-gray-700' : 'bg-gray-100'}
              `}>
                <input
                  type="text"
                  placeholder="Ask about companies..."
                  className={`
                    flex-1 bg-transparent border-none outline-none text-sm
                    ${isDark
                      ? 'text-white placeholder:text-gray-400'
                      : 'text-gray-900 placeholder:text-gray-500'
                    }
                  `}
                />
                <button
                  className={`
                    p-1.5 rounded transition-colors
                    ${isDark
                      ? 'hover:bg-gray-600 text-gray-300'
                      : 'hover:bg-gray-200 text-gray-600'
                    }
                  `}
                >
                  <Send size={14} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}