import React from 'react';
import { Mail, Lock, User, School2 } from 'lucide-react';
import { FieldWrapper } from './FieldWrapper';
import { UniversityDropdown } from '../UniversityDropdown';

interface AccountStepProps {
  name: string;
  setName: (name: string) => void;
  university: string;
  setUniversity: (university: string) => void;
  email: string;
  setEmail: (email: string) => void;
  password: string;
  setPassword: (password: string) => void;
  validationField: string | null;
  validationMessage: string;
  onValidationClose: () => void;
  onInputChange: (field: string, value: string, setter: (value: string) => void) => void;
  onFieldFocus?: (field: string) => void;
}

export function AccountStep({
  name,
  setName,
  university,
  setUniversity,
  email,
  setEmail,
  password,
  setPassword,
  validationField,
  validationMessage,
  onValidationClose,
  onInputChange,
  onFieldFocus
}: AccountStepProps) {
  return (
    <>
      <FieldWrapper 
        icon={<User size={18} />} 
        field="name"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <input 
          type="text" 
          value={name} 
          onChange={e => onInputChange('name', e.target.value, setName)}
          placeholder="Full name" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
          onFocus={() => onFieldFocus && onFieldFocus('name')}
        />
      </FieldWrapper>

      <FieldWrapper 
        icon={<School2 size={18} />} 
        field="university"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <UniversityDropdown 
          value={university} 
          onChange={(value) => onInputChange('university', value, setUniversity)} 
          onFocus={() => onFieldFocus && onFieldFocus('university')}
        />
      </FieldWrapper>

      <FieldWrapper 
        icon={<Mail size={18} />} 
        field="email"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <input 
          type="email" 
          value={email} 
          onChange={e => onInputChange('email', e.target.value, setEmail)}
          placeholder="Email address" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
          onFocus={() => onFieldFocus && onFieldFocus('email')}
        />
      </FieldWrapper>

      <FieldWrapper 
        icon={<Lock size={18} />} 
        field="password"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <input 
          type="password" 
          value={password} 
          onChange={e => onInputChange('password', e.target.value, setPassword)}
          placeholder="Password" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
          onFocus={() => onFieldFocus && onFieldFocus('password')}
        />
      </FieldWrapper>
    </>
  );
} 