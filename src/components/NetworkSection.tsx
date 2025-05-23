import React, { useState } from 'react';
import { Search, ArrowUpRight, Mail, Building2 } from 'lucide-react';

interface Connection {
  name: string;
  avatar: string;
  role: string;
  company: string;
  companyLogo: string;
  yaleClass: string;
  email: string;
}

interface NetworkSectionProps {
  isDark: boolean;
  connections: Connection[];
}

export function NetworkSection({ isDark, connections = [] }: NetworkSectionProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const filterConnections = (search: string) => {
    if (!search) return connections;
    const searchLower = search.toLowerCase();
    return connections.filter(connection => 
      connection.name.toLowerCase().includes(searchLower) ||
      connection.role.toLowerCase().includes(searchLower) ||
      connection.company.toLowerCase().includes(searchLower)
    );
  };

  return (
    <div className={`
      rounded-xl border overflow-hidden
      ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
    `}>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className={`text-lg font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Network
            </h2>
            <p className={`text-sm mt-1 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
              Connect with industry professionals
            </p>
          </div>
        </div>

        <div className={`
          flex items-center gap-2 px-3 py-2 rounded-lg mb-6
          ${isDark ? 'bg-gray-700/50' : 'bg-gray-50'}
        `}>
          <Search size={14} className={isDark ? 'text-gray-400' : 'text-gray-500'} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search connections..."
            className={`
              w-full bg-transparent border-none outline-none text-sm
              ${isDark
                ? 'text-white placeholder:text-gray-400'
                : 'text-gray-900 placeholder:text-gray-500'
              }
            `}
          />
        </div>

        <div className="space-y-2">
          {connections && connections.length > 0 ? (
            filterConnections(searchQuery).map((connection, index) => (
              <div
                key={index}
                className={`
                  p-4 rounded-lg transition-colors
                  ${isDark ? 'bg-gray-700/50 hover:bg-gray-700' : 'bg-gray-50 hover:bg-gray-100'}
                `}
              >
                <div className="flex items-center gap-4">
                  <img
                    src={connection.avatar}
                    alt={connection.name}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h4 className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                        {connection.name}
                      </h4>
                      <span className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                        Yale '{connection.yaleClass}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                        {connection.role} at {connection.company}
                      </span>
                      <img
                        src={connection.companyLogo}
                        alt={connection.company}
                        className="w-4 h-4 rounded bg-white"
                      />
                    </div>
                  </div>
                  <button
                    className={`
                      p-2 rounded-lg transition-colors
                      ${isDark
                        ? 'hover:bg-gray-600 text-gray-400 hover:text-gray-300'
                        : 'hover:bg-gray-200 text-gray-500 hover:text-gray-700'
                      }
                    `}
                  >
                    <Mail size={16} />
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className={`text-center py-6 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
              No connections found
            </div>
          )}
        </div>
      </div>
    </div>
  );
}