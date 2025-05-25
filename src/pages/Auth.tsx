import React, { useState, useCallback, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, ChevronRight, Mail, Lock } from 'lucide-react';
import { WizardStep } from '../types/auth/types';
import { dummyResumeData } from '../utils/auth/constants';
import { AccountStep } from '../components/auth/AccountStep';
import { ProfessionalStep } from '../components/auth/ProfessionalStep';
import { ResumeReviewStep } from '../components/auth/ResumeReviewStep';
import { ClarityStep } from '../components/auth/ClarityStep';
import { InterestStep } from '../components/auth/InterestStep';
import { CompanyStep } from '../components/auth/CompanyStep';

interface AuthProps {
  onLogin: () => void;
}

export function Auth({ onLogin }: AuthProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [step, setStep] = useState<WizardStep>(WizardStep.Account);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [university, setUniversity] = useState('');
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [clarity, setClarity] = useState<'yes' | 'no' | null>(null);
  const [selectedCompanies, setSelectedCompanies] = useState<Set<string>>(new Set());
  const [selectedInterests, setSelectedInterests] = useState<Set<string>>(new Set());
  const [resume, setResume] = useState<File | null>(null);
  const [resumeData, setResumeData] = useState(dummyResumeData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [validationField, setValidationField] = useState<string | null>(null);

  const required = (field: string, value: string, label?: string) => {
    if (!value) {
      setValidationField(field);
      setValidationMessage(`Please ${label || `enter your ${field}`}`);
      return false;
    }
    return true;
  };

  const validateStep = () => {
    setValidationField(null);
    setValidationMessage('');

    switch (step) {
      case WizardStep.Account:
        if (!required('name', name)) return false;
        if (!required('university', university)) return false;
        if (!required('email', email)) return false;
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          setValidationField('email');
          setValidationMessage('Please enter a valid email address');
          return false;
        }
        if (!required('password', password)) return false;
        if (password.length < 6) {
          setValidationField('password');
          setValidationMessage('Password must be at least 6 characters');
          return false;
        }
        return true;

      case WizardStep.Professional:
        if (linkedinUrl && !/^https?:\/\/(www\.)?linkedin\.com\/in\/[\w-]+\/?$/.test(linkedinUrl)) {
          setValidationField('linkedin');
          setValidationMessage('Please enter a valid LinkedIn URL');
          return false;
        }
        if (!resume) {
          setValidationField('resume');
          setValidationMessage('Please upload your resume');
          return false;
        }
        return true;

      case WizardStep.ResumeReview:
        return true;

      case WizardStep.Clarity:
        if (!clarity) {
          setValidationField('clarity');
          setValidationMessage('Please select an option');
          return false;
        }
        return true;

      case WizardStep.Interests:
      case WizardStep.Companies:
        return true;
    }
    return true;
  };

  const goNext = () => {
    if (!validateStep()) return;
    
    if (step < WizardStep.Companies) {
      setStep(prev => (prev + 1) as WizardStep);
    } else {
      handleFinalSubmit();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isLogin) {
      if (!(required('email', email) && required('password', password))) return;
      setLoading(true);
      // Demo login - simulate API call
      setTimeout(() => {
        setLoading(false);
        onLogin();
      }, 1000);
    } else {
      goNext();
    }
  };

  const handleFinalSubmit = () => {
    setLoading(true);
    // Demo signup - simulate API call
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 1500);
  };

  const handleInputChange = (field: string, value: string, setter: (value: string) => void) => {
    setter(value);
    if (validationField === field) {
      setValidationField(null);
      setValidationMessage('');
    }
  };

  const dotCount = useMemo(() => 6, []);

  useEffect(() => {
    if (validationField && validationMessage) {
      const timeout = setTimeout(() => {
        setValidationField(null);
        setValidationMessage('');
      }, 3000);
      return () => clearTimeout(timeout);
    }
  }, [validationField, validationMessage]);

  const clearValidation = () => {
    setValidationField(null);
    setValidationMessage('');
  };

  const handleFieldFocus = (field: string) => {
    if (validationField === field) {
      clearValidation();
    }
  };

  const renderStep = () => {
    switch (step) {
      case WizardStep.Account:
        return (
          <AccountStep
            name={name}
            setName={setName}
            university={university}
            setUniversity={setUniversity}
            email={email}
            setEmail={setEmail}
            password={password}
            setPassword={setPassword}
            validationField={validationField}
            validationMessage={validationMessage}
            onValidationClose={clearValidation}
            onInputChange={handleInputChange}
            onFieldFocus={handleFieldFocus}
          />
        );
      case WizardStep.Professional:
        return (
          <ProfessionalStep
            linkedinUrl={linkedinUrl}
            setLinkedinUrl={setLinkedinUrl}
            resume={resume}
            setResume={setResume}
            validationField={validationField}
            validationMessage={validationMessage}
            onValidationClose={clearValidation}
            onInputChange={handleInputChange}
            onFieldFocus={handleFieldFocus}
          />
        );
      case WizardStep.ResumeReview:
        return <ResumeReviewStep resumeData={resumeData} />;
      case WizardStep.Clarity:
        return (
          <ClarityStep
            clarity={clarity}
            setClarity={setClarity}
            validationField={validationField}
            validationMessage={validationMessage}
            onValidationClose={clearValidation}
            onFieldFocus={handleFieldFocus}
          />
        );
      case WizardStep.Interests:
        return (
          <InterestStep
            selectedInterests={selectedInterests}
            setSelectedInterests={setSelectedInterests}
            clarity={clarity}
            onFieldFocus={handleFieldFocus}
          />
        );
      case WizardStep.Companies:
        return (
          <CompanyStep
            selectedCompanies={selectedCompanies}
            setSelectedCompanies={setSelectedCompanies}
            clarity={clarity}
            onFieldFocus={handleFieldFocus}
          />
        );
    }
  };

  const stepTitles = {
    [WizardStep.Account]: 'Create your account',
    [WizardStep.Professional]: 'Professional details',
    [WizardStep.ResumeReview]: 'Review your information',
    [WizardStep.Clarity]: 'Career clarity',
    [WizardStep.Interests]: 'Your interests',
    [WizardStep.Companies]: clarity === 'yes' ? 'Dream companies' : 'Companies that inspire you'
  };

  const stepSubtitles = {
    [WizardStep.Account]: 'Start your journey with Milo',
    [WizardStep.Professional]: 'Help us personalize your experience',
    [WizardStep.ResumeReview]: 'We\'ve parsed your resume automatically',
    [WizardStep.Clarity]: 'Tell us where you\'re at',
    [WizardStep.Interests]: clarity === 'yes' 
      ? 'Pick topics that align with your goals'
      : 'Pick topics that intrigue you',
    [WizardStep.Companies]: clarity === 'yes'
      ? 'Pick companies you have in mind'
      : 'These help us understand what excites you'
  };

  const getButtonText = () => {
    if (isLogin) return 'Sign In';
    if (step < WizardStep.Companies) return 'Next';
    return 'Create Account';
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)]
            [background-size:16px_16px] opacity-40"/>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-gray-50 to-gray-50"/>
      </div>

      <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden relative">
          <div className="p-8 max-h-[80vh] overflow-y-auto" onClick={clearValidation}>
            <div className="flex items-center justify-center mb-8">
              <img src="/logo.png" alt="Milo" className="h-24 w-auto object-contain" />
            </div>

            <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
              {isLogin ? 'Welcome back' : stepTitles[step]}
            </h2>

            <p className="text-center text-gray-600 mb-8">
              {isLogin ? 'Sign in to continue to Milo' : stepSubtitles[step]}
            </p>

            <form onSubmit={handleSubmit} className="space-y-4" onClick={e => e.stopPropagation()}>
              <AnimatePresence mode="wait">
                <motion.div
                  key={`${isLogin}-${step}`}
                  initial={{opacity:0,x:20}} 
                  animate={{opacity:1,x:0}} 
                  exit={{opacity:0,x:-20}}
                  className="space-y-4">
                  {isLogin ? (
                    <>
                      <div className="relative">
                        <input
                          type="email"
                          value={email}
                          onChange={e => setEmail(e.target.value)}
                          placeholder="Email address"
                          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                        />
                        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10 flex-shrink-0">
                          <Mail size={18} />
                        </span>
                      </div>
                      <div className="relative">
                        <input
                          type="password"
                          value={password}
                          onChange={e => setPassword(e.target.value)}
                          placeholder="Password"
                          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                        />
                        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10 flex-shrink-0">
                          <Lock size={18} />
                        </span>
                      </div>
                    </>
                  ) : renderStep()}
                </motion.div>
              </AnimatePresence>

              {error && (
                <motion.div initial={{opacity:0,y:-10}} animate={{opacity:1,y:0}}
                  className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">
                  {error}
                </motion.div>
              )}

              {(isLogin || step === WizardStep.Companies) && (
                <button type="submit" disabled={loading}
                  className="w-full bg-blue-600 text-white rounded-lg px-4 py-2 font-medium
                             hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                             focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed
                             transition-colors relative">
                  <span className={loading ? 'invisible' : 'visible'}>
                    {getButtonText()}
                  </span>
                  {loading && <Loader2 size={20}
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-spin"/>}
                </button>
              )}
            </form>

            <div className="mt-6 text-center">
              <button onClick={() => {
                setIsLogin(!isLogin);
                setStep(WizardStep.Account);
                setError('');
                setValidationField(null);
                setValidationMessage('');
              }}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium focus:outline-none">
                {isLogin ? "Don't have an account?" : 'Already have an account?'}
              </button>
            </div>
          </div>

          {!isLogin && step > WizardStep.Account && (
            <div className="absolute bottom-4 left-4">
              <button
                type="button"
                onClick={() => setStep(prev => (prev - 1) as WizardStep)}
                className="flex items-center text-sm text-gray-600 hover:text-gray-700 transition-colors bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200 hover:border-gray-300"
              >
                <ChevronRight size={16} className="mr-1 rotate-180" />
                Back
              </button>
            </div>
          )}

          {!isLogin && step < WizardStep.Companies && (
            <div className="absolute bottom-4 right-4">
              <button
                type="button"
                onClick={goNext}
                className="flex items-center text-sm text-blue-600 hover:text-blue-700 transition-colors bg-white px-4 py-2 rounded-lg shadow-sm border border-blue-200 hover:border-blue-300"
              >
                Next
                <ChevronRight size={16} className="ml-1" />
              </button>
            </div>
          )}
        </div>

        {!isLogin && (
          <div className="mt-4 flex justify-center gap-2">
            {Array.from({length: dotCount}, (_,i) => i + 1).map(i => (
              <div key={i}
                   className={`w-2 h-2 rounded-full transition-colors
                    ${i === step ? 'bg-blue-600' : 'bg-gray-300'}`}/>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default Auth;