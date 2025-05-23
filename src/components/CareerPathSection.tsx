import React from 'react';
import { Brain, Code, Cloud, Database, LineChart, Network } from 'lucide-react';
import { CareerPathFlow } from './CareerPathFlow';

interface CareerPathSectionProps {
  isDark: boolean;
}

export function CareerPathSection({ isDark }: CareerPathSectionProps) {
  return (
    <div className={`
      rounded-xl border overflow-hidden
      ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
    `}>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className={`text-lg font-semibold flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              <Brain size={18} className="text-purple-500" />
              Career Path Insights
            </h2>
            <p className={`text-sm mt-1 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
              Explore potential career paths based on your skills and interests
            </p>
          </div>
        </div>

        <div className="mt-4">
          <CareerPathFlow />
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              title: "AI/ML Engineering",
              growth: "+45%",
              trend: "up",
              description: "Strong match with your ML and Python skills",
              companies: ["OpenAI", "Anthropic", "DeepMind"],
              avgSalary: "$180K - $250K",
              icon: <Brain size={16} className="text-purple-500" />
            },
            {
              title: "Full Stack Development",
              growth: "+28%",
              trend: "up",
              description: "Leverages your React and Node.js expertise",
              companies: ["Stripe", "Vercel", "MongoDB"],
              avgSalary: "$150K - $220K",
              icon: <Code size={16} className="text-blue-500" />
            },
            {
              title: "Cloud Architecture",
              growth: "+32%",
              trend: "up",
              description: "Growing demand for AWS knowledge",
              companies: ["Snowflake", "Databricks", "HashiCorp"],
              avgSalary: "$160K - $230K",
              icon: <Cloud size={16} className="text-sky-500" />
            }
          ].map((path, index) => (
            <div
              key={index}
              className={`
                p-4 rounded-lg border
                ${isDark ? 'bg-gray-700/50 border-gray-600' : 'bg-gray-50 border-gray-200'}
              `}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {path.icon}
                  <h3 className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {path.title}
                  </h3>
                </div>
                <div className="text-xs font-medium text-emerald-500">
                  {path.growth}
                </div>
              </div>
              
              <p className={`mt-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
                {path.description}
              </p>

              <div className="mt-3">
                <div className={`text-xs font-medium mb-1 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                  Top Companies
                </div>
                <div className="flex flex-wrap gap-1">
                  {path.companies.map((company, i) => (
                    <span
                      key={i}
                      className={`
                        text-xs px-2 py-0.5 rounded
                        ${isDark ? 'bg-gray-600 text-gray-300' : 'bg-gray-200 text-gray-700'}
                      `}
                    >
                      {company}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-3">
                <div className={`text-xs font-medium mb-1 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                  Average Salary
                </div>
                <div className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {path.avgSalary}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}