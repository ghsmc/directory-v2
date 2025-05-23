import React, { useState, useRef, useEffect } from 'react';
import { Sun, Moon, Palette, Search, Check } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';

interface ThemeSelectorProps {
  isDark: boolean;
  activeTheme: string;
  onThemeChange: (theme: string) => void;
  onDarkModeChange: (isDark: boolean) => void;
}

export function ThemeSelector({ isDark, activeTheme, onThemeChange, onDarkModeChange }: ThemeSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const { themes } = useTheme();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredThemes = themes.filter(theme => 
    theme.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleThemeSelect = (themeName: string, isDarkTheme: boolean) => {
    onThemeChange(themeName);
    onDarkModeChange(isDarkTheme);
    setIsOpen(false);
  };

  return (
    <div ref={containerRef} className="relative theme-selector">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          p-2 rounded-lg flex items-center gap-2 transition-colors
          ${isDark ? 'text-white/80 hover:bg-white/5' : 'text-gray-600 hover:bg-gray-100'}
        `}
      >
        <Palette size={20} />
      </button>

      <div
        className={`
          absolute right-0 top-full mt-2 w-64 p-2
          rounded-xl shadow-xl border backdrop-blur-xl z-50
          transition-all duration-200 origin-top-right font-mono
          ${isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'}
          ${isDark ? 'bg-gray-900/90 border-white/10' : 'bg-white/90 border-gray-200'}
        `}
      >
        <div className={`
          p-2 mb-2 rounded-lg flex items-center gap-2
          ${isDark ? 'bg-white/5' : 'bg-gray-100'}
        `}>
          <Search size={14} className={isDark ? 'text-white/40' : 'text-gray-400'} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="search themes..."
            className={`
              w-full bg-transparent border-none outline-none text-sm font-mono tracking-tight
              ${isDark ? 'text-white placeholder:text-white/40' : 'text-gray-900 placeholder:text-gray-500'}
            `}
          />
        </div>

        <div className="max-h-[300px] overflow-y-auto space-y-1">
          {/* Quick access themes */}
          <div className="flex gap-1 mb-2">
            <button
              onClick={() => handleThemeSelect('light', false)}
              className={`
                flex-1 p-2 rounded-lg text-left flex items-center justify-between tracking-tight
                ${activeTheme === 'light' ? 'bg-gray-100' : 'hover:bg-gray-50'}
              `}
              style={{
                backgroundColor: '#ffffff',
                color: '#111827'
              }}
            >
              <div className="flex items-center gap-2">
                <Sun size={14} />
                <span>light</span>
              </div>
              {activeTheme === 'light' && <Check size={14} />}
            </button>
            <button
              onClick={() => handleThemeSelect('dark', true)}
              className={`
                flex-1 p-2 rounded-lg text-left flex items-center justify-between tracking-tight
                ${activeTheme === 'dark' ? 'bg-white/10' : 'hover:bg-white/5'}
              `}
              style={{
                backgroundColor: '#111827',
                color: '#f3f4f6'
              }}
            >
              <div className="flex items-center gap-2">
                <Moon size={14} />
                <span>dark</span>
              </div>
              {activeTheme === 'dark' && <Check size={14} />}
            </button>
          </div>

          <div className={`h-px mb-2 ${isDark ? 'bg-white/10' : 'bg-gray-200'}`} />

          {filteredThemes.filter(theme => !['light', 'dark'].includes(theme.name)).map((theme) => (
            <button
              key={theme.name}
              onClick={() => handleThemeSelect(
                theme.name,
                theme.bgColor.startsWith('#0') || theme.bgColor.startsWith('#1') || theme.bgColor.startsWith('#2')
              )}
              className={`
                w-full flex items-center justify-between p-2 rounded-lg text-left tracking-tight
                ${theme.name === activeTheme
                  ? isDark
                    ? 'bg-white/10'
                    : 'bg-gray-100'
                  : isDark
                  ? 'hover:bg-white/5'
                  : 'hover:bg-gray-50'
                }
              `}
            >
              <div className="flex items-center gap-3">
                <div className="flex gap-1">
                  <div
                    className="w-4 h-4 rounded-full ring-1 ring-black/5"
                    style={{ backgroundColor: theme.mainColor }}
                  />
                  <div
                    className="w-4 h-4 rounded-full ring-1 ring-black/5"
                    style={{ backgroundColor: theme.subColor }}
                  />
                </div>
                <span 
                  className={`text-sm ${isDark ? 'text-white/90' : 'text-gray-900'}`}
                >
                  {theme.name}
                </span>
              </div>
              {activeTheme === theme.name && (
                <Check size={14} className={isDark ? 'text-white/80' : 'text-gray-600'} />
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}