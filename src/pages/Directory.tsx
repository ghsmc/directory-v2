import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, ArrowUpRight, MapPin, ChevronDown, ChevronUp, Building2, MessageSquare } from 'lucide-react';
import { mockPeople } from '../data/mockPeople';
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

export function Directory() {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedPerson, setExpandedPerson] = useState<string | null>(null);
  const [savedProfiles, setSavedProfiles] = useState<Set<string>>(new Set());
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleSaveProfile = (personId: string) => {
    setSavedProfiles(prev => {
      const next = new Set(prev);
      if (next.has(personId)) {
        next.delete(personId);
      } else {
        next.add(personId);
      }
      return next;
    });
  };

  const toggleExpanded = (personId: string) => {
    setExpandedPerson(current => current === personId ? null : personId);
  };

  const filteredPeople = mockPeople.filter(person => {
    const matchesSearch = 
      person.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.currentRole.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.currentCompany.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.bio.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.skills.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()));

    return matchesSearch;
  });

  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px]">
        {/* Directory Listing */}
        <div className="h-[calc(100vh-8rem)] overflow-y-auto">
          <div className="max-w-7xl mx-auto px-4 pb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-4">
              {filteredPeople.map((person) => (
                <motion.div
                  key={person.id}
                  variants={cardVariants}
                  className="relative bg-white border border-gray-200 rounded-lg overflow-hidden hover:border-gray-300 transition-all duration-200"
                >
                  <div className="p-4">
                    <div className="flex gap-3">
                      {/* Profile images section */}
                      <div className="flex flex-col items-center gap-1.5 w-10">
                        <motion.img
                          src={person.avatar}
                          alt={person.name}
                          className="w-10 h-10 rounded-full object-cover ring-2 ring-white shadow-sm"
                          whileHover={{ scale: 1.05 }}
                          transition={{ duration: 0.2 }}
                        />
                        <motion.img
                          src={person.companyLogo}
                          alt={person.currentCompany}
                          className="w-10 h-10 rounded-lg object-contain bg-white p-1.5 border border-gray-200"
                          whileHover={{ scale: 1.05 }}
                          transition={{ duration: 0.2 }}
                        />
                        <motion.img
                          src={person.schoolLogo}
                          alt={person.education[0].school}
                          className="w-10 h-10 rounded-lg object-contain bg-white p-1.5 border border-gray-200"
                          whileHover={{ scale: 1.05 }}
                          transition={{ duration: 0.2 }}
                        />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0">
                            <h3 className="text-sm font-semibold text-gray-900 truncate">
                              {person.name}
                            </h3>
                            <div className="mt-0.5">
                              <span className="text-xs font-medium text-gray-900">
                                {person.currentRole}
                              </span>
                            </div>
                            <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                              <MapPin size={12} />
                              <span className="truncate">{person.location}</span>
                            </div>
                          </div>
                          
                          <div className="flex flex-col items-end gap-1">
                            <div className="flex items-center gap-1">
                              <span className="text-[10px] font-medium text-gray-400">MATCH</span>
                              <div className="px-1.5 py-0.5 text-[10px] font-medium text-white bg-emerald-500 rounded">
                                {person.matchScore}
                              </div>
                            </div>
                            <motion.button
                              onClick={() => toggleSaveProfile(person.id)}
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.95 }}
                              className={`
                                p-1 rounded-md transition-colors duration-200
                                ${savedProfiles.has(person.id)
                                  ? 'text-yellow-500 hover:bg-yellow-50'
                                  : 'text-gray-400 hover:bg-gray-100'
                                }
                              `}
                            >
                              <Star size={14} fill={savedProfiles.has(person.id) ? 'currentColor' : 'none'} />
                            </motion.button>
                          </div>
                        </div>

                        <div className="mt-2 flex flex-wrap gap-1">
                          {person.skills.slice(0, 3).map((skill) => (
                            <motion.span
                              key={skill}
                              whileHover={{ scale: 1.05 }}
                              className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-blue-50 text-blue-600"
                            >
                              {skill}
                            </motion.span>
                          ))}
                          {person.skills.length > 3 && (
                            <motion.span
                              whileHover={{ scale: 1.05 }}
                              className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-gray-100 text-gray-600"
                            >
                              +{person.skills.length - 3}
                            </motion.span>
                          )}
                        </div>

                        <div className="mt-2 flex justify-end">
                          <motion.button
                            onClick={() => toggleExpanded(person.id)}
                            className="flex items-center gap-0.5 text-xs text-gray-500 hover:text-gray-700 transition-colors duration-200 p-1"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                          >
                            {expandedPerson === person.id ? (
                              <ChevronUp size={14} />
                            ) : (
                              <ChevronDown size={14} />
                            )}
                          </motion.button>
                        </div>

                        <AnimatePresence>
                          {expandedPerson === person.id && (
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
                                    Experience
                                  </h4>
                                  <div className="space-y-3">
                                    {person.experience.map((exp, index) => (
                                      <motion.div 
                                        key={index} 
                                        className="flex gap-2"
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                      >
                                        <img
                                          src={exp.companyLogo}
                                          alt={exp.company}
                                          className="w-6 h-6 rounded bg-white object-contain flex-shrink-0 border border-gray-200"
                                        />
                                        <div>
                                          <div className="text-xs font-medium text-gray-900">
                                            {exp.role}
                                          </div>
                                          <div className="text-[11px] text-gray-600">
                                            {exp.company}
                                          </div>
                                          <div className="text-[11px] text-gray-500">
                                            {exp.duration} • {exp.location}
                                          </div>
                                          <div className="mt-0.5 text-[11px] text-gray-600">
                                            {exp.description}
                                          </div>
                                        </div>
                                      </motion.div>
                                    ))}
                                  </div>
                                </div>

                                <div>
                                  <h4 className="text-xs font-medium text-gray-900 mb-2">Education</h4>
                                  <div className="space-y-3">
                                    {person.education.map((edu, index) => (
                                      <motion.div 
                                        key={index}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                      >
                                        <div className="text-xs font-medium text-gray-900">
                                          {edu.school}
                                        </div>
                                        <div className="text-[11px] text-gray-600">
                                          {edu.degree} in {edu.field}
                                        </div>
                                        <div className="text-[11px] text-gray-500">
                                          Class of {edu.year}
                                          {edu.gpa && ` • GPA: ${edu.gpa}`}
                                        </div>
                                      </motion.div>
                                    ))}
                                  </div>
                                </div>

                                <div className="flex justify-end">
                                  <a
                                    href={`mailto:${person.email}`}
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