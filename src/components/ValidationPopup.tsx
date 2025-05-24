import React from 'react';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';

interface ValidationPopupProps {
  message: string;
  show: boolean;
  onClose: () => void;
}

export function ValidationPopup({ message, show, onClose }: ValidationPopupProps) {
  if (!show) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      className="absolute -bottom-12 left-0 z-50 bg-red-50 rounded-lg shadow-lg border border-red-200 p-3 flex items-center gap-2"
      role="alert"
      aria-live="assertive"
    >
      <AlertCircle className="w-5 h-5 text-red-400" />
      <span className="text-sm text-red-700">{message}</span>
    </motion.div>
  );
}