import React from 'react';
import { motion } from 'framer-motion';

interface MetricsBarProps {
  isDark: boolean;
  metrics: {
    tokensUsed: number;
  };
}

export function MetricsBar({ isDark, metrics }: MetricsBarProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`
        p-4 rounded-xl border relative overflow-hidden
        ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
      `}
    >
      <div className="flex items-center justify-center gap-3">
        <img 
          src="https://thumb.ac-illust.com/f3/f3cf90c7866487298e571d271a5f5564_t.jpeg"
          alt="Token"
          className="w-12 h-12 object-contain"
        />
        <div className={`
          font-pixel text-3xl tracking-wider
          ${isDark ? 'text-amber-400' : 'text-amber-600'}
          drop-shadow-[0_1px_1px_rgba(0,0,0,0.1)]
        `}>
          {metrics.tokensUsed.toLocaleString()}
        </div>
      </div>
    </motion.div>
  );
}