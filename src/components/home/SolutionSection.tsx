import React from 'react';
import { DropdownText } from './DropdownText';

export function SolutionSection() {
  return (
    <div>
      <h3 className="text-xl lg:text-2xl font-bold text-gray-900 mb-6 lg:mb-8">
        The Solution
      </h3>
      <div className="space-y-4 lg:space-y-6">
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-50 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-emerald-600 text-sm">1</span>
            </span>
            <div className="flex-1">
              <DropdownText 
                title="Milo makes discovery simple, fast, and personal."
                content="Milo is a real-time, AI-powered search engine that surfaces the right opportunities the moment a student starts looking — no filters, no fluff, just answers that matter."
              />
            </div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-emerald-50 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-emerald-600 text-sm">2</span>
            </span>
            <div className="flex-1">
              <DropdownText 
                title="It's built for how young people think — not how systems work."
                content="Milo uses conversational AI and live webscraping to deliver results based on intent, not keywords. It's search that feels like dialogue — fast, dynamic, and purpose-driven."
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}