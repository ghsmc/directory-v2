import React from 'react';
import { Linkedin, Upload, Check } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import { FieldWrapper } from './FieldWrapper';

interface ProfessionalStepProps {
  linkedinUrl: string;
  setLinkedinUrl: (url: string) => void;
  resume: File | null;
  setResume: (file: File | null) => void;
  validationField: string | null;
  validationMessage: string;
  onValidationClose: () => void;
  onInputChange: (field: string, value: string, setter: (value: string) => void) => void;
  onFieldFocus?: (field: string) => void;
}

export function ProfessionalStep({
  linkedinUrl,
  setLinkedinUrl,
  resume,
  setResume,
  validationField,
  validationMessage,
  onValidationClose,
  onInputChange,
  onFieldFocus
}: ProfessionalStepProps) {
  const onDrop = React.useCallback((files: File[]) => {
    if (files.length > 0) {
      setResume(files[0]);
      if (validationField === 'resume') {
        onValidationClose();
      }
    }
  }, [validationField, onValidationClose, setResume]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1
  });

  return (
    <>
      <FieldWrapper 
        icon={<Linkedin size={18} />} 
        field="linkedin"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <input 
          type="url" 
          value={linkedinUrl} 
          onChange={e => onInputChange('linkedin', e.target.value, setLinkedinUrl)}
          placeholder="LinkedIn URL (optional)" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
          onFocus={() => onFieldFocus && onFieldFocus('linkedin')}
        />
      </FieldWrapper>

      <FieldWrapper 
        field="resume"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={onValidationClose}
      >
        <div {...getRootProps()} className="cursor-pointer">
          <input {...getInputProps()} />
          <div className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors
                ${isDragActive ? 'border-blue-500 bg-blue-50' : 
                  resume ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-gray-400'}`}>
            {resume ? (
              <>
                <Check className="mx-auto h-12 w-12 text-green-500"/>
                <p className="mt-2 text-sm text-green-700 font-medium">{resume.name}</p>
                <p className="mt-1 text-xs text-green-600">Click to change</p>
              </>
            ) : (
              <>
                <Upload className="mx-auto h-12 w-12 text-gray-400"/>
                <p className="mt-2 text-sm text-gray-600">
                  Drop your resume here, or click to select
                </p>
                <p className="mt-1 text-xs text-gray-500">PDF up to 10MB</p>
              </>
            )}
          </div>
        </div>
      </FieldWrapper>
    </>
  );
} 