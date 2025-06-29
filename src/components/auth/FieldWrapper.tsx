import React from 'react';
import { ValidationPopup } from '../ValidationPopup';

interface FieldWrapperProps {
  children: React.ReactNode;
  icon: React.ReactNode;
  field: string;
  validationField: string | null;
  validationMessage: string;
  onClose: () => void;
}

export function FieldWrapper({
  children,
  icon,
  field,
  validationField,
  validationMessage,
  onClose
}: FieldWrapperProps) {
  const show = field && field === validationField;
  
  return (
    <div className="relative">
      <div className="relative">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10 flex-shrink-0">
          {icon}
        </span>
        {children}
      </div>
      {show && (
        <ValidationPopup
          message={validationMessage}
          show
          onClose={onClose}
        />
      )}
    </div>
  );
} 