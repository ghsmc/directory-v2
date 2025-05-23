import React from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (value: string) => void;
}

export function SearchBar({ value, onChange, onSubmit }: SearchBarProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(value);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search size={16} className="text-gray-400" />
        </div>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="block w-full pl-10 pr-4 py-2 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-200 
                   focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all duration-200
                   placeholder:text-xs placeholder:text-gray-400"
          placeholder="Search jobs, companies, or people..."
        />
      </div>
    </form>
  );
}