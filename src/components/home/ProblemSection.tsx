import React from 'react';
import { DropdownText } from './DropdownText';

export function ProblemSection() {
  return (
    <div className="pb-8 lg:pb-0">
      <h3 className="text-xl lg:text-2xl font-bold text-gray-900 mb-6 lg:mb-8">
        The Problem
      </h3>
      <div className="space-y-4 lg:space-y-6">
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-red-50 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-red-600 text-sm">1</span>
            </span>
            <div className="flex-1">
              <DropdownText 
                title="Predefined paths are limiting potential."
                content="Students are pushed into narrow, oversaturated pipelines. Platforms like LinkedIn prioritize ads and recruiter incentives over personal fit — promoting what pays, not what aligns."
              />
            </div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-red-50 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-red-600 text-sm">2</span>
            </span>
            <div className="flex-1">
              <DropdownText 
                title="Opportunity is fragmented and hidden."
                content="Jobs, research labs, clubs, and courses are scattered across outdated portals, obscure web pages, and word-of-mouth networks. Most students don't even know what exists — let alone how to access it."
              />
            </div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <span className="w-6 h-6 rounded-full bg-red-50 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="text-red-600 text-sm">3</span>
            </span>
            <div className="flex-1">
              <DropdownText 
                title="The result is quiet failure."
                content="Brilliant people get passed over. They give up on what excites them and default to what feels &quot;safe.&quot; Burnout, disengagement, and misalignment follow — not from lack of talent, but lack of discovery."
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}