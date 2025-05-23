import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Menu, ExternalLink } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { UIPreview } from '../UIPreview';

interface HeroSectionProps {
  inView: boolean;
}

const categories = [
  { name: 'JOBS', color: 'bg-blue-50 text-blue-600 border-blue-100' },
  { name: 'COMPANIES', color: 'bg-red-50 text-red-600 border-red-100' },
  { name: 'PEOPLE', color: 'bg-yellow-50 text-yellow-600 border-yellow-100' }
];

const recommendations = {
  jobs: [
    {
      title: 'ML Engineer',
      company: 'OpenAI',
      logo: 'https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      location: 'San Francisco, CA',
      salary: '$200K - $350K'
    },
    {
      title: 'Research Scientist',
      company: 'Anthropic',
      logo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      location: 'San Francisco, CA',
      salary: '$180K - $300K'
    },
    {
      title: 'AI Engineer',
      company: 'DeepMind',
      logo: 'https://img.logo.dev/deepmind.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      location: 'London, UK',
      salary: '£150K - £250K'
    }
  ],
  companies: [
    {
      name: 'OpenAI',
      logo: 'https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'Leading AI research company',
      valuation: '$80B'
    },
    {
      name: 'Anthropic',
      logo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI safety and research',
      valuation: '$4.1B'
    },
    {
      name: 'DeepMind',
      logo: 'https://img.logo.dev/deepmind.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
      description: 'AI research and applications',
      valuation: 'Part of Google'
    }
  ],
  people: [
    {
      name: 'Sarah Chen',
      role: 'ML Engineer at OpenAI',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
      matchScore: 95
    },
    {
      name: 'Michael Park',
      role: 'Research Scientist at Anthropic',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e',
      matchScore: 92
    },
    {
      name: 'Emily Zhang',
      role: 'Software Engineer at DeepMind',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
      matchScore: 90
    }
  ]
};

export function HeroSection({ inView }: HeroSectionProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  const menuItems = [
    { title: 'CONVICTION', href: '/conviction' },
    { title: "WHAT'S NEXT", href: '#whats-next' },
    { title: 'TEAM', href: '#team' }
  ];

  return (
    <div className="flex flex-col lg:flex-row items-start justify-between">
      {/* Left Content */}
      <div className="w-full lg:w-1/4 flex-shrink-0 px-4 sm:px-8 lg:px-8 mb-8 lg:mb-0">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="flex flex-col items-start"
        >
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-4">
              <img 
                src="https://gmccain.com/milo.png"
                alt="Milo"
                className="w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 rounded-xl shadow-lg"
              />
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900">
                Milo
              </h2>
            </div>
          </div>

          <p className="text-lg sm:text-xl lg:text-2xl text-gray-600 leading-relaxed mt-4 sm:mt-6 mb-6 sm:mb-8">
            Find work you actually want. Talk to real people. Get hired.
          </p>

          <div className="flex flex-wrap gap-1.5 mb-6 sm:mb-8">
            {categories.map((category, index) => (
              <span
                key={index}
                className={`px-2 py-1 rounded-md text-xs font-medium border ${category.color}`}
              >
                {category.name}
              </span>
            ))}
          </div>

          <div className="flex flex-col gap-3 w-full lg:w-auto">
            <Link
              to="/jobs"
              className="group relative px-6 py-3 rounded-lg text-white font-medium text-base
                bg-gray-900 hover:bg-gray-800 transition-all duration-200 text-center lg:text-left"
            >
              <div className="relative flex items-center justify-center lg:justify-start gap-2">
                Start Discovering
                <ArrowRight size={18} className="transition-transform duration-200 group-hover:translate-x-0.5" />
              </div>
            </Link>
          </div>

          {/* Recommendations Section */}
          <div className="mt-8 space-y-6 w-full">
            <h3 className="text-lg font-semibold text-gray-900">Recommended for you</h3>
            
            <div className="space-y-4">
              {/* Jobs */}
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-sm font-medium text-gray-900">Top Jobs</h4>
                  <Link to="/jobs" className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    View all
                    <ExternalLink size={12} />
                  </Link>
                </div>
                <div className="space-y-3">
                  {recommendations.jobs.map((job, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                      <img src={job.logo} alt={job.company} className="w-8 h-8 rounded bg-white object-contain" />
                      <div className="min-w-0">
                        <div className="text-sm font-medium text-gray-900 truncate">{job.title}</div>
                        <div className="text-xs text-gray-500 truncate">{job.company} • {job.location}</div>
                        <div className="text-xs text-emerald-600 font-medium mt-0.5">{job.salary}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Companies */}
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-sm font-medium text-gray-900">Top Companies</h4>
                  <Link to="/companies" className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    View all
                    <ExternalLink size={12} />
                  </Link>
                </div>
                <div className="space-y-3">
                  {recommendations.companies.map((company, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                      <img src={company.logo} alt={company.name} className="w-8 h-8 rounded bg-white object-contain" />
                      <div className="min-w-0">
                        <div className="text-sm font-medium text-gray-900 truncate">{company.name}</div>
                        <div className="text-xs text-gray-500 truncate">{company.description}</div>
                        <div className="text-xs text-gray-600 font-medium mt-0.5">{company.valuation} valuation</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* People */}
              <div className="p-4 bg-white rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-sm font-medium text-gray-900">People to Follow</h4>
                  <Link to="/directory" className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    View all
                    <ExternalLink size={12} />
                  </Link>
                </div>
                <div className="space-y-3">
                  {recommendations.people.map((person, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer">
                      <img src={person.avatar} alt={person.name} className="w-8 h-8 rounded-full object-cover" />
                      <div className="min-w-0 flex-1">
                        <div className="text-sm font-medium text-gray-900 truncate">{person.name}</div>
                        <div className="text-xs text-gray-500 truncate">{person.role}</div>
                      </div>
                      <div className="px-1.5 py-0.5 text-xs font-medium text-white bg-emerald-500 rounded">
                        {person.matchScore}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Demo Section */}
      <div className="w-full lg:w-3/4 pl-0 lg:pl-12 hidden md:block">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={inView ? { opacity: 1, scale: 1, y: 0 } : {}}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="w-full px-4 lg:px-0"
        >
          <UIPreview />
        </motion.div>
      </div>

      {/* Menu Button and Dropdown */}
      <div className="fixed top-4 right-4 z-50">
        <div className="relative">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="p-2 rounded-lg bg-white hover:bg-gray-50 transition-colors duration-200 shadow-lg"
          >
            <Menu size={24} className="text-gray-600" />
          </button>

          <AnimatePresence>
            {isMenuOpen && (
              <>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
                  onClick={() => setIsMenuOpen(false)}
                />
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ type: "spring", stiffness: 300, damping: 25 }}
                  className="absolute right-0 top-full mt-2 w-48 py-2 bg-white rounded-lg shadow-xl border border-gray-200 z-50"
                >
                  {menuItems.map((item) => (
                    <button
                      key={item.title}
                      onClick={() => {
                        setIsMenuOpen(false);
                        if (item.href.startsWith('/')) {
                          navigate(item.href);
                        }
                      }}
                      className="w-full px-4 py-2 text-left text-sm tracking-wide font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50/80 transition-colors duration-200"
                    >
                      {item.title}
                    </button>
                  ))}
                </motion.div>
              </>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}