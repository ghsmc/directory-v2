import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star, ArrowUpRight, MapPin, ChevronDown, ChevronUp, Building2, MessageSquare, Users } from 'lucide-react';
import { companies, jobs } from '../services/mockData';
import { mockPeople } from '../data/mockPeople';
import { AIChatModal } from '../components/AIChatModal';
import { Navbar } from '../components/Navbar';

// Combine and shuffle feed items
const feedItems = [
  ...companies.map(item => ({ ...item, type: 'company' })),
  ...jobs.map(item => ({ ...item, type: 'job' })),
  ...mockPeople.map(item => ({ ...item, type: 'person' }))
].sort(() => Math.random() - 0.5);

export function Feed() {
  const [savedItems, setSavedItems] = useState<Set<string>>(new Set());
  const [expandedItem, setExpandedItem] = useState<string | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'for-you' | 'following'>('for-you');

  const toggleSaveItem = (id: string) => {
    setSavedItems(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const toggleExpanded = (id: string) => {
    setExpandedItem(current => current === id ? null : id);
  };

  const renderFeedItem = (item: any) => {
    switch (item.type) {
      case 'company':
        return (
          <div className="flex gap-3">
            <img
              src={item.logo}
              alt={item.name}
              className="w-10 h-10 rounded-lg object-contain bg-white border border-gray-200"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-gray-900 truncate flex items-center gap-2">
                    {item.name}
                    <ArrowUpRight size={14} className="text-gray-400" />
                  </h3>
                  <div className="mt-0.5">
                    <span className="text-xs font-medium text-gray-900">
                      {item.industry}
                    </span>
                  </div>
                  <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                    <Building2 size={12} />
                    <span className="truncate">{item.jobCount} open roles</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-1">
                  <div className="flex items-center gap-1">
                    <span className="text-[10px] font-medium text-gray-400">MATCH</span>
                    <div className="px-1.5 py-0.5 text-[10px] font-medium text-white bg-emerald-500 rounded">
                      {item.matchScore}
                    </div>
                  </div>
                  <motion.button
                    onClick={() => toggleSaveItem(item.id)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className={`
                      p-1 rounded-md transition-colors duration-200
                      ${savedItems.has(item.id)
                        ? 'text-yellow-500 hover:bg-yellow-50'
                        : 'text-gray-400 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Star size={14} fill={savedItems.has(item.id) ? 'currentColor' : 'none'} />
                  </motion.button>
                </div>
              </div>

              <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                {item.description}
              </p>

              <div className="mt-2 flex items-center gap-2">
                <div className="text-xs text-gray-500">
                  {item.jobCount} open positions
                </div>
                <span className="text-gray-300">•</span>
                <div className="text-xs text-gray-500">
                  {item.valuation} valuation
                </div>
              </div>
            </div>
          </div>
        );

      case 'job':
        return (
          <div className="flex gap-3">
            <img
              src={item.logoUrl}
              alt={item.company}
              className="w-10 h-10 rounded-lg object-contain bg-white border border-gray-200"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-gray-900 truncate flex items-center gap-2">
                    {item.title}
                    <ArrowUpRight size={14} className="text-gray-400" />
                  </h3>
                  <div className="mt-0.5">
                    <span className="text-xs font-medium text-gray-900">
                      {item.company}
                    </span>
                  </div>
                  <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                    <MapPin size={12} />
                    <span className="truncate">{item.location}</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-1">
                  <div className="text-xs font-medium text-emerald-600">
                    {item.salary}
                  </div>
                  <motion.button
                    onClick={() => toggleSaveItem(item.id)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className={`
                      p-1 rounded-md transition-colors duration-200
                      ${savedItems.has(item.id)
                        ? 'text-yellow-500 hover:bg-yellow-50'
                        : 'text-gray-400 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Star size={14} fill={savedItems.has(item.id) ? 'currentColor' : 'none'} />
                  </motion.button>
                </div>
              </div>

              <div className="mt-2 flex flex-wrap gap-1">
                {item.skills.slice(0, 3).map((skill: string) => (
                  <span
                    key={skill}
                    className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-blue-50 text-blue-600"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        );

      case 'person':
        return (
          <div className="flex gap-3">
            <img
              src={item.avatar}
              alt={item.name}
              className="w-10 h-10 rounded-full object-cover border border-gray-200"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-gray-900 truncate flex items-center gap-2">
                    {item.name}
                    <ArrowUpRight size={14} className="text-gray-400" />
                  </h3>
                  <div className="mt-0.5">
                    <span className="text-xs font-medium text-gray-900">
                      {item.currentRole}
                    </span>
                  </div>
                  <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-500">
                    <Users size={12} />
                    <span className="truncate">{item.currentCompany}</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-1">
                  <div className="flex items-center gap-1">
                    <span className="text-[10px] font-medium text-gray-400">MATCH</span>
                    <div className="px-1.5 py-0.5 text-[10px] font-medium text-white bg-emerald-500 rounded">
                      {item.matchScore}
                    </div>
                  </div>
                  <motion.button
                    onClick={() => toggleSaveItem(item.id)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className={`
                      p-1 rounded-md transition-colors duration-200
                      ${savedItems.has(item.id)
                        ? 'text-yellow-500 hover:bg-yellow-50'
                        : 'text-gray-400 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Star size={14} fill={savedItems.has(item.id) ? 'currentColor' : 'none'} />
                  </motion.button>
                </div>
              </div>

              <div className="mt-2 flex flex-wrap gap-1">
                {item.skills.slice(0, 3).map((skill: string) => (
                  <span
                    key={skill}
                    className="px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-purple-50 text-purple-600"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px]">
        {/* Fixed Header */}
        <div className="fixed top-0 inset-x-0 z-40 bg-white border-b border-gray-200 md:left-[72px]">
          <div className="max-w-2xl mx-auto px-4">
            <div className="flex items-center justify-center h-[72px]">
              <div className="flex items-center gap-8">
                <button
                  onClick={() => setActiveTab('for-you')}
                  className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                    activeTab === 'for-you' ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  For You
                  {activeTab === 'for-you' && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
                      initial={false}
                    />
                  )}
                </button>
                <button
                  onClick={() => setActiveTab('following')}
                  className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                    activeTab === 'following' ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Following
                  {activeTab === 'following' && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
                      initial={false}
                    />
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Feed Content */}
        <div className="max-w-2xl mx-auto px-4 pb-24">
          <div className="space-y-4 pt-4">
            {feedItems.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-xl border border-gray-200 overflow-hidden"
              >
                <div className="p-4">
                  {renderFeedItem(item)}
                </div>
              </motion.div>
            ))}
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

        {/* Chat Modal */}
        <AIChatModal 
          isOpen={isChatOpen} 
          onClose={() => setIsChatOpen(false)}
        />
      </div>
    </div>
  );
}