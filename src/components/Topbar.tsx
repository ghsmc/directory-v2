import React, { useState, useRef, useEffect } from 'react';
import { Search } from 'lucide-react';

interface TopbarProps {
  isDark?: boolean;
}

export function Topbar({ isDark }: TopbarProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsSearchFocused(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="fixed top-0 left-0 right-0 z-40 bg-white md:left-[72px]">
      <div className="flex items-center h-[72px] px-4 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <img 
            src="/logo.png"
            alt="Milo"
            className="w-12 h-12 rounded-lg object-contain"
          />
        </div>

        {/* Search Container */}
        <div className="flex-1 max-w-xl mx-4">
          <div 
            ref={searchRef}
            className="relative w-full bg-gray-50 rounded-lg border border-gray-200"
          >
            <div className="flex items-center h-9">
              <Search size={14} className="ml-3 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setIsSearchFocused(true)}
                placeholder="Search..."
                className="w-full bg-transparent border-none outline-none text-[13px] pl-2 pr-4 text-gray-900 placeholder:text-gray-400"
              />
            </div>
          </div>
        </div>

        <button className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
          <div className="w-[22px] h-[22px] rounded-full bg-gray-300" />
        </button>
      </div>
    </div>
  );
}