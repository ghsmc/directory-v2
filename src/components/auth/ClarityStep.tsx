import React from 'react';
import { ValidationPopup } from '../ValidationPopup';

interface ClarityStepProps {
  clarity: 'yes' | 'no' | null;
  setClarity: (clarity: 'yes' | 'no' | null) => void;
  validationField: string | null;
  validationMessage: string;
  onValidationClose: () => void;
  onFieldFocus?: (field: string) => void;
}

export function ClarityStep({
  clarity,
  setClarity,
  validationField,
  validationMessage,
  onValidationClose,
  onFieldFocus
}: ClarityStepProps) {
  return (
    <div className="space-y-6">
      <p className="text-center text-gray-700 font-medium">
        Do you already know <em>what</em> you want to do?
      </p>
      <div className="flex justify-center gap-6">
        {(['yes', 'no'] as const).map(opt => (
          <button key={opt}
            type="button"
            onClick={() => {
              setClarity(opt);
              if (validationField === 'clarity') {
                onValidationClose();
              }
            }}
            onFocus={() => onFieldFocus && onFieldFocus('clarity')}
            className={`px-6 py-3 rounded-lg transition-colors text-sm font-medium
              ${clarity === opt
                ? 'bg-blue-100 text-blue-700 border border-blue-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-transparent'
              }`}>
            {opt === 'yes' ? 'Yes' : 'Not yet'}
          </button>
        ))}
      </div>
      {validationField === 'clarity' && (
        <ValidationPopup 
          message={validationMessage} 
          show 
          onClose={onValidationClose} 
        />
      )}
    </div>
  );
} 