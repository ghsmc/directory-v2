import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, ArrowUpRight, MapPin, ChevronDown, ChevronUp, Building2, MessageSquare } from 'lucide-react';
import { companies } from '../services/mockData';
import { AIChatModal } from '../components/AIChatModal';
import { Navbar } from '../components/Navbar';

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0.23, 1, 0.32, 1]
    }
  }
};

const expandVariants = {
  hidden: { 
    height: 0, 
    opacity: 0,
    transition: {
      height: { duration: 0.3, ease: [0.23, 1, 0.32, 1] },
      opacity: { duration: 0.2 }
    }
  },
  visible: { 
    height: 'auto', 
    opacity: 1,
    transition: {
      height: { duration: 0.3, ease: [0.23, 1, 0.32, 1] },
      opacity: { duration: 0.2, delay: 0.1 }
    }
  }
};

export function Companies() {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedCompany, setExpandedCompany] = useState<string | null>(null);
  const [savedCompanies, setSavedCompanies] = useState<Set<string>>(new Set());
  const [isChatOpen, setIsChatOpen] = useState(false);

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

  const filteredCompanies = companies.filter(company => {
    const matchesSearch = 
      company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.industry.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesSearch;
  });

  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px]">
        {/* Companies Listing */}
        <div className="h-[calc(100vh-8rem)] overflow-y-auto">
          <div className="max-w-7xl mx-auto px-4 pb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-4">
              {filteredCompanies.map((company) => (
                <motion.div
                  key={company.id}
                  variants={cardVariants}
                  className="relative bg-white border border-gray-200 rounded-lg overflow-hidden hover:border-gray-300 transition-all duration-200"
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
                            <h3 className="text-sm font-semibold text-gray-900 truncate">
                              {company.name}
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
                              variants={expandVariants}
                              initial="hidden"
                              animate="visible"
                              exit="hidden"
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

                                <div className="flex justify-end">
                                  <a
                                    href={`mailto:contact@${company.name.toLowerCase()}.com`}
                                    className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-700"
                                  >
                                    <ArrowUpRight size={12} />
                                    Contact
                                  </a>
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

        {/* Mobile chat button */}
        <div className="fixed bottom-20 right-4 lg:hidden">
          <button
            onClick={() => setIsChatOpen(true)}
            className="p-4 bg-blue-600 text-white rounded-full shadow-lg"
          >
            <MessageSquare size={24} />
          </button>
        </div>

        <AIChatModal isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      </div>
    </div>
  );
}