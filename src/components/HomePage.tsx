import React from 'react';
import { useInView } from 'react-intersection-observer';
import { DotPattern } from './DotPattern';
import { Star, ArrowUpRight, MapPin, ChevronDown, ChevronUp, Building2, MessageSquare } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { companies } from '../services/mockData';
import { AIChatModal } from './AIChatModal';
import { Navbar } from './Navbar';

interface HomePageProps {
  isDark: boolean;
}

const categories = [
  { id: 'all', label: 'All', active: true },
  { id: 'following', label: 'Following', active: false },
  { id: 'recommended', label: 'Recommended', active: false },
];

export function HomePage({ isDark }: HomePageProps) {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const [savedCompanies, setSavedCompanies] = React.useState<Set<string>>(new Set());
  const [expandedCompany, setExpandedCompany] = React.useState<string | null>(null);
  const [isChatOpen, setIsChatOpen] = React.useState(false);
  const [activeCategory, setActiveCategory] = React.useState('all');

  const toggleSaveCompany = (companyId: string) => {
    setSavedCompanies(prev => {
      const next = new Set(prev);
      if (next.has(companyId)) {
        next.delete(companyId);
      } else {
        next.add(companyId);
      }
      return next;
    });
  };

  const toggleExpanded = (companyId: string) => {
    setExpandedCompany(current => current === companyId ? null : companyId);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Fixed Header */}
      <div className="fixed top-0 inset-x-0 z-40 bg-white border-b border-gray-200">
        <div className="max-w-2xl mx-auto px-4">
          <div className="flex items-center justify-center h-16">
            <div className="flex items-center gap-3">
              <img 
                src="https://gmccain.com/milo.png"
                alt="MILO"
                className="w-8 h-8 rounded-xl"
              />
              <span className="text-lg font-bold tracking-wide text-gray-900">MILO</span>
            </div>
          </div>

          {/* Category Tags */}
          <div className="flex items-center gap-2 pb-3">
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`
                  px-4 py-1.5 rounded-full text-sm font-medium transition-colors
                  ${activeCategory === category.id
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }
                `}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Scrollable Feed */}
      <div className="pt-28 pb-20 h-screen overflow-y-auto">
        <div className="relative">
          {/* Background */}
          <div className="fixed inset-0 -z-10">
            <DotPattern />
          </div>

          {/* Feed Content */}
          <div className="relative max-w-2xl mx-auto px-4 py-4">
            <div className="space-y-4">
              {companies.map((company) => (
                <motion.div
                  key={company.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-xl border border-gray-200 overflow-hidden"
                >
                  <div className="p-4">
                    <div className="flex gap-3">
                      <img
                        src={company.logo}
                        alt={company.name}
                        className="w-10 h-10 rounded-lg object-contain bg-white border border-gray-200"
                      />
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0">
                            <h3 className="text-sm font-semibold text-gray-900 truncate flex items-center gap-2">
                              {company.name}
                              <ArrowUpRight size={14} className="text-gray-400" />
                            </h3>
                            <div className="mt-0.5">
                              <span className="text-xs font-medium text-gray-900">
                                {company.industry}
                              </span>
                            </div>
                            <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                              <MapPin size={12} />
                              <span className="truncate">San Francisco, CA</span>
                            </div>
                          </div>
                          
                          <div className="flex flex-col items-end gap-1">
                            <div className="flex items-center gap-1">
                              <span className="text-[10px] font-medium text-gray-400">MATCH</span>
                              <div className="px-1.5 py-0.5 text-[10px] font-medium text-white bg-emerald-500 rounded">
                                {company.matchScore}
                              </div>
                            </div>
                            <motion.button
                              onClick={() => toggleSaveCompany(company.id)}
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.95 }}
                              className={`
                                p-1 rounded-md transition-colors duration-200
                                ${savedCompanies.has(company.id)
                                  ? 'text-yellow-500 hover:bg-yellow-50'
                                  : 'text-gray-400 hover:bg-gray-100'
                                }
                              `}
                            >
                              <Star size={14} fill={savedCompanies.has(company.id) ? 'currentColor' : 'none'} />
                            </motion.button>
                          </div>
                        </div>

                        <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                          {company.description}
                        </p>

                        <div className="mt-2 flex items-center gap-2">
                          <div className="text-xs text-gray-500">
                            {company.jobCount} open positions
                          </div>
                          <span className="text-gray-300">•</span>
                          <div className="text-xs text-gray-500">
                            {company.valuation} valuation
                          </div>
                        </div>

                        {/* Dropdown button */}
                        <div className="mt-2 flex justify-end">
                          <motion.button
                            onClick={() => toggleExpanded(company.id)}
                            className="flex items-center gap-0.5 text-xs text-gray-500 hover:text-gray-700 transition-colors duration-200 p-1"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                          >
                            {expandedCompany === company.id ? (
                              <ChevronUp size={14} />
                            ) : (
                              <ChevronDown size={14} />
                            )}
                          </motion.button>
                        </div>

                        <AnimatePresence>
                          {expandedCompany === company.id && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="mt-2 pt-2 border-t border-gray-200"
                            >
                              <div className="space-y-4">
                                <div>
                                  <h4 className="text-xs font-medium text-gray-900 mb-2 flex items-center gap-1">
                                    <Building2 size={14} />
                                    Company Details
                                  </h4>
                                  <div className="space-y-2 text-xs">
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Status</span>
                                      <span className="text-gray-900">{company.status}</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Founded</span>
                                      <span className="text-gray-900">2021</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Team Size</span>
                                      <span className="text-gray-900">100-500</span>
                                    </div>
                                  </div>
                                </div>

                                <div>
                                  <h4 className="text-xs font-medium text-gray-900 mb-2">Recent News</h4>
                                  <div className="space-y-2">
                                    <a href="#" className="block text-xs text-blue-600 hover:underline">
                                      Raised $100M Series B funding
                                    </a>
                                    <a href="#" className="block text-xs text-blue-600 hover:underline">
                                      Launched new AI product
                                    </a>
                                  </div>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Chat Button */}
      <motion.button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-20 right-4 z-50 p-4 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <MessageSquare size={24} />
      </motion.button>

      {/* Chat Modal */}
      <AIChatModal isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

      {/* Bottom Navigation */}
      <Navbar />
    </div>
  );
}