import React, { ReactNode } from 'react';
import { ValidationPopup } from './ValidationPopup';

interface FieldWrapperProps {
  icon: ReactNode;
  field: string;
  validationField: string | null;
  validationMessage: string;
  onClose: () => void;
  children: ReactNode;
}

export function FieldWrapper({
  icon,
  field,
  validationField,
  validationMessage,
  onClose,
  children
}: FieldWrapperProps) {
  return (
    <div className="relative">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {icon}
        </div>
        {children}
      </div>
      {validationField === field && (
        <ValidationPopup
          message={validationMessage}
          show
          onClose={onClose}
        />
      )}
    </div>
  );
} 