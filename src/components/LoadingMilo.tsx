import React from 'react';
import { motion } from 'framer-motion';

interface LoadingMiloProps {
  isDark: boolean;
}

export function LoadingMilo({ isDark }: LoadingMiloProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      className={`flex items-center gap-2 ${isDark ? 'text-white/60' : 'text-gray-500'}`}
    >
      <motion.div className="relative">
        <motion.span
          initial={{ opacity: 0.3 }}
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "linear"
          }}
          className="text-[14px]"
        >
          Analyzing
        </motion.span>
      </motion.div>
      <motion.div className="flex items-center gap-1">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: [0, 1, 0], y: [-1, 1, -1] }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              delay: i * 0.3,
              ease: "easeInOut"
            }}
            className="w-1 h-1 rounded-full bg-current"
          />
        ))}
      </motion.div>
    </motion.div>
  );
}