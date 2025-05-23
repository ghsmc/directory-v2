import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Search } from 'lucide-react';

interface University {
  name: string;
  logo: string;
}

interface UniversityDropdownProps {
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
}

const universities: University[] = [
  { name: 'Yale University', logo: 'https://img.logo.dev/yale.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Harvard University', logo: 'https://img.logo.dev/harvard.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Princeton University', logo: 'https://img.logo.dev/princeton.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'MIT', logo: 'https://img.logo.dev/mit.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Stanford University', logo: 'https://img.logo.dev/stanford.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Columbia University', logo: 'https://img.logo.dev/columbia.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'University of Pennsylvania', logo: 'https://img.logo.dev/upenn.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Brown University', logo: 'https://img.logo.dev/brown.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Dartmouth College', logo: 'https://img.logo.dev/dartmouth.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' },
  { name: 'Cornell University', logo: 'https://img.logo.dev/cornell.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ' }
];

export function UniversityDropdown({ value, onChange, required = false }: UniversityDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (isOpen && searchRef.current) {
      searchRef.current.focus();
    }
  }, [isOpen]);

  const selectedUniversity = universities.find(uni => uni.name === value);

  const filteredUniversities = universities.filter(uni =>
    uni.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div ref={dropdownRef} className="relative w-full">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center gap-3 pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all bg-white text-left"
      >
        <div className="flex items-center gap-3 flex-1 min-w-0">
          {selectedUniversity ? (
            <>
              <img
                src={selectedUniversity.logo}
                alt={selectedUniversity.name}
                className="w-6 h-6 object-contain flex-shrink-0"
              />
              <span className="text-gray-900 truncate">{selectedUniversity.name}</span>
            </>
          ) : (
            <span className="text-gray-500">Select your university</span>
          )}
        </div>
        <ChevronDown
          size={18}
          className={`text-gray-400 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden"
          >
            <div className="p-2">
              <div className="relative">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  ref={searchRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search universities..."
                  className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="max-h-64 overflow-y-auto">
              {filteredUniversities.map((uni) => (
                <button
                  key={uni.name}
                  type="button"
                  onClick={() => {
                    onChange(uni.name);
                    setIsOpen(false);
                    setSearchQuery('');
                  }}
                  className={`
                    w-full flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-colors
                    ${value === uni.name ? 'bg-blue-50' : ''}
                  `}
                >
                  <img
                    src={uni.logo}
                    alt={uni.name}
                    className="w-6 h-6 object-contain flex-shrink-0"
                  />
                  <span className="text-sm text-gray-900 truncate">{uni.name}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Hidden input for form validation */}
      <input
        type="text"
        value={value}
        onChange={() => {}}
        required={required}
        className="sr-only"
        tabIndex={-1}
      />
    </div>
  );
}