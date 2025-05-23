import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, ArrowUpRight, MapPin, ChevronDown, ChevronUp, Building2, MessageSquare } from 'lucide-react';
import { jobs } from '../services/mockData';
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

export function Jobs() {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedJob, setExpandedJob] = useState<string | null>(null);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleSaveJob = (jobId: string) => {
    setSavedJobs(prev => {
      const next = new Set(prev);
      if (next.has(jobId)) {
        next.delete(jobId);
      } else {
        next.add(jobId);
      }
      return next;
    });
  };

  const toggleExpanded = (jobId: string) => {
    setExpandedJob(current => current === jobId ? null : jobId);
  };

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = 
      job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.skills.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesSearch;
  });

  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px]">
        {/* Jobs Listing */}
        <div className="h-[calc(100vh-8rem)] overflow-y-auto">
          <div className="max-w-7xl mx-auto px-4 pb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-4">
              {filteredJobs.map((job) => (
                <motion.div
                  key={job.id}
                  variants={cardVariants}
                  className="relative bg-white border border-gray-200 rounded-lg overflow-hidden hover:border-gray-300 transition-all duration-200"
                >
                  <div className="p-4">
                    <div className="flex gap-3">
                      <img
                        src={job.logoUrl}
                        alt={job.company}
                        className="w-10 h-10 rounded-lg object-contain bg-white border border-gray-200"
                      />
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0">
                            <h3 className="text-sm font-semibold text-gray-900 truncate flex items-center gap-2">
                              {job.title}
                              <ArrowUpRight size={14} className="text-gray-400" />
                            </h3>
                            <div className="mt-0.5">
                              <span className="text-xs font-medium text-gray-900">
                                {job.company}
                              </span>
                            </div>
                            <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                              <MapPin size={12} />
                              <span className="truncate">{job.location}</span>
                            </div>
                          </div>
                          
                          <div className="flex flex-col items-end gap-1">
                            <div className="text-xs font-medium text-emerald-600">
                              {job.salary}
                            </div>
                            <motion.button
                              onClick={() => toggleSaveJob(job.id)}
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.95 }}
                              className={`
                                p-1 rounded-md transition-colors duration-200
                                ${savedJobs.has(job.id)
                                  ? 'text-yellow-500 hover:bg-yellow-50'
                                  : 'text-gray-400 hover:bg-gray-100'
                                }
                              `}
                            >
                              <Star size={14} fill={savedJobs.has(job.id) ? 'currentColor' : 'none'} />
                            </motion.button>
                          </div>
                        </div>

                        <div className="mt-2 flex flex-wrap gap-1">
                          {job.skills.slice(0, 3).map((skill) => (
                            <span
                              key={skill}
                              className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-blue-50 text-blue-600"
                            >
                              {skill}
                            </span>
                          ))}
                          {job.skills.length > 3 && (
                            <span
                              className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-gray-100 text-gray-600"
                            >
                              +{job.skills.length - 3}
                            </span>
                          )}
                        </div>

                        <div className="mt-2 flex justify-end">
                          <motion.button
                            onClick={() => toggleExpanded(job.id)}
                            className="flex items-center gap-0.5 text-xs text-gray-500 hover:text-gray-700 transition-colors duration-200 p-1"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                          >
                            {expandedJob === job.id ? (
                              <ChevronUp size={14} />
                            ) : (
                              <ChevronDown size={14} />
                            )}
                          </motion.button>
                        </div>

                        <AnimatePresence>
                          {expandedJob === job.id && (
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
                                    Job Details
                                  </h4>
                                  <div className="space-y-2 text-xs">
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Employment Type</span>
                                      <span className="text-gray-900">{job.employmentType}</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Experience Level</span>
                                      <span className="text-gray-900">{job.experienceLevel}</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-gray-500">Remote</span>
                                      <span className="text-gray-900">{job.remote ? 'Yes' : 'No'}</span>
                                    </div>
                                  </div>
                                </div>

                                <div>
                                  <h4 className="text-xs font-medium text-gray-900 mb-2">Description</h4>
                                  <p className="text-xs text-gray-600">{job.description}</p>
                                </div>

                                <div>
                                  <h4 className="text-xs font-medium text-gray-900 mb-2">Requirements</h4>
                                  <ul className="space-y-1">
                                    {job.requirements.map((req, index) => (
                                      <li key={index} className="text-xs text-gray-600 flex items-center gap-2">
                                        <div className="w-1 h-1 rounded-full bg-gray-400" />
                                        {req}
                                      </li>
                                    ))}
                                  </ul>
                                </div>

                                <div className="flex justify-end">
                                  <button
                                    className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                                  >
                                    Apply Now
                                  </button>
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