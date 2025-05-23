import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

export function Conviction() {
  return (
    <>
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <Link
              to="/"
              className="flex items-center gap-2 px-2 py-1 -ml-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
            >
              <ArrowLeft size={20} />
              <span>Back</span>
            </Link>
            <div className="flex items-center">
              <img 
                src="https://gmccain.com/milo.png"
                alt="Milo"
                className="h-8 w-8 rounded-lg"
              />
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 text-center mb-4">
          Our Convictions
        </h1>
        <p className="text-lg text-gray-600 text-center mb-12">
          Test content for scrolling
        </p>

        {Array.from({ length: 50 }).map((_, i) => (
          <div 
            key={i}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6"
          >
            <h2 className="text-xl font-semibold text-gray-900">
              Test Section {i + 1}
            </h2>
            <p className="text-gray-600 mt-2">
              This is a test section to verify scrolling functionality.
              Adding some more text to ensure we have enough content to scroll.
              The quick brown fox jumps over the lazy dog.
            </p>
          </div>
        ))}
      </div>
    </>
  );
}

export default Conviction;