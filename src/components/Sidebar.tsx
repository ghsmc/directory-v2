import React from 'react';
import { CircleDot } from 'lucide-react';

interface NavSection {
  title: string;
  items: {
    label: string;
    count?: number;
    isActive?: boolean;
  }[];
}

const navigation: NavSection[] = [
  {
    title: 'Tech Trends',
    items: [
      { label: 'Live', isActive: true }
    ]
  },
  {
    title: 'Job Market',
    items: [
      { label: 'Open Tech Jobs', count: 233802 },
      { label: 'Tech Layoffs' },
      { label: 'Big Tech Hiring' },
      { label: 'Tech Jobs Overview' },
      { label: 'Remote Index' }
    ]
  },
  {
    title: 'Companies and Sectors',
    items: [
      { label: "Top Co's" },
      { label: "Hottest Co's by Sector" },
      { label: "Hottest Co's by Investor" },
      { label: 'Sector Reports' }
    ]
  },
  {
    title: 'Locations',
    items: [
      { label: 'Top Tech Cities' },
      { label: 'Top Tech Countries' }
    ]
  }
];

interface SidebarProps {
  isDark: boolean;
}

export function Sidebar({ isDark }: SidebarProps) {
  return (
    <div 
      className={`
        w-64 h-screen overflow-y-auto fixed left-0 top-0 bottom-0
        ${isDark ? 'bg-black border-white/10' : 'bg-white border-gray-200'}
        border-r
      `}
    >
      <div className="p-4">
        <div className="flex items-center gap-3 px-2 py-3">
          <img 
            src="https://img.logo.dev/milo.dev?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ"
            alt="Milo"
            className="w-8 h-8"
          />
          <span className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
            milo
          </span>
        </div>

        <div className="mt-6">
          {navigation.map((section, index) => (
            <div key={index} className="mb-6">
              <h2 className={`
                text-sm font-medium mb-2 px-2
                ${isDark ? 'text-white/60' : 'text-gray-500'}
              `}>
                {section.title}
              </h2>
              <ul className="space-y-1">
                {section.items.map((item, itemIndex) => (
                  <li key={itemIndex}>
                    <a
                      href="#"
                      className={`
                        flex items-center justify-between px-2 py-1.5 rounded-lg text-[13px]
                        ${item.isActive
                          ? isDark
                            ? 'bg-white/10 text-white'
                            : 'bg-gray-100 text-gray-900'
                          : isDark
                            ? 'text-white/80 hover:bg-white/5'
                            : 'text-gray-700 hover:bg-gray-50'
                        }
                      `}
                    >
                      <span className="flex items-center gap-2">
                        {item.isActive && (
                          <span className="flex items-center gap-1 text-emerald-500">
                            <CircleDot size={14} />
                            <span>Live</span>
                          </span>
                        )}
                        {!item.isActive && item.label}
                      </span>
                      {item.count && (
                        <span className={`
                          text-xs font-medium
                          ${isDark ? 'text-white/40' : 'text-gray-500'}
                        `}>
                          {item.count.toLocaleString()}
                        </span>
                      )}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}