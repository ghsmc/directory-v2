import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { createClient } from '@supabase/supabase-js';
import { useDropzone } from 'react-dropzone';
import { Mail, Lock, User, ArrowRight, Loader2, Upload, Linkedin, Briefcase, Heart, School2 } from 'lucide-react';
import { UniversityDropdown } from '../components/UniversityDropdown';
import { ValidationPopup } from '../components/ValidationPopup';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

const interests = [
  'Artificial Intelligence',
  'Machine Learning',
  'Web Development',
  'Mobile Development',
  'Cloud Computing',
  'Data Science',
  'Cybersecurity',
  'Blockchain',
  'DevOps',
  'UI/UX Design'
];

const companies = [
  'Google',
  'Meta',
  'Apple',
  'Microsoft',
  'Amazon',
  'OpenAI',
  'Anthropic',
  'Tesla',
  'SpaceX',
  'Stripe'
];

const universities = [
  'Yale University',
  'Harvard University',
  'Princeton University',
  'MIT',
  'Stanford University',
  'Columbia University',
  'University of Pennsylvania',
  'Brown University',
  'Dartmouth College',
  'Cornell University'
];

export function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [university, setUniversity] = useState('');
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [selectedInterests, setSelectedInterests] = useState<Set<string>>(new Set());
  const [selectedCompanies, setSelectedCompanies] = useState<Set<string>>(new Set());
  const [resume, setResume] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1);
  const [validationMessage, setValidationMessage] = useState('');
  const [validationField, setValidationField] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setResume(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  const toggleInterest = (interest: string) => {
    setSelectedInterests(prev => {
      const next = new Set(prev);
      if (next.has(interest)) {
        next.delete(interest);
      } else {
        next.add(interest);
      }
      return next;
    });
  };

  const toggleCompany = (company: string) => {
    setSelectedCompanies(prev => {
      const next = new Set(prev);
      if (next.has(company)) {
        next.delete(company);
      } else {
        next.add(company);
      }
      return next;
    });
  };

  const validateField = (field: string, value: string) => {
    if (!value && field === 'name') {
      setValidationMessage('Please enter your full name');
      setValidationField('name');
      return false;
    }
    if (!value && field === 'university') {
      setValidationMessage('Please select your university');
      setValidationField('university');
      return false;
    }
    if (!value && field === 'email') {
      setValidationMessage('Please enter your email address');
      setValidationField('email');
      return false;
    }
    if (!value && field === 'password') {
      setValidationMessage('Please enter your password');
      setValidationField('password');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear previous validation messages
    setValidationMessage('');
    setValidationField(null);

    // Validate required fields
    if (!isLogin) {
      if (step === 1) {
        if (!validateField('name', name)) return;
        if (!validateField('university', university)) return;
        if (!validateField('email', email)) return;
        if (!validateField('password', password)) return;
      }
    } else {
      if (!validateField('email', email)) return;
      if (!validateField('password', password)) return;
    }

    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (error) throw error;
      } else {
        if (step < 3) {
          setStep(step + 1);
          setLoading(false);
          return;
        }

        const { error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              full_name: name,
              university,
              linkedin_url: linkedinUrl,
              interests: Array.from(selectedInterests),
              target_companies: Array.from(selectedCompanies)
            },
          },
        });
        if (error) throw error;

        // Upload resume if provided
        if (resume) {
          const { error: uploadError } = await supabase.storage
            .from('resumes')
            .upload(`${email}/resume.pdf`, resume);
          if (uploadError) throw uploadError;
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <>
            <div className="relative">
              <User
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
              />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Full name"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              />
              <ValidationPopup
                message={validationMessage}
                show={validationField === 'name'}
                onClose={() => setValidationField(null)}
              />
            </div>

            <div className="relative">
              <School2
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10"
              />
              <UniversityDropdown
                value={university}
                onChange={setUniversity}
              />
              <ValidationPopup
                message={validationMessage}
                show={validationField === 'university'}
                onClose={() => setValidationField(null)}
              />
            </div>

            <div className="relative">
              <Mail
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email address"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              />
              <ValidationPopup
                message={validationMessage}
                show={validationField === 'email'}
                onClose={() => setValidationField(null)}
              />
            </div>

            <div className="relative">
              <Lock
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              />
              <ValidationPopup
                message={validationMessage}
                show={validationField === 'password'}
                onClose={() => setValidationField(null)}
              />
            </div>
          </>
        );

      case 2:
        return (
          <>
            <div className="relative">
              <Linkedin
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
              />
              <input
                type="url"
                value={linkedinUrl}
                onChange={(e) => setLinkedinUrl(e.target.value)}
                placeholder="LinkedIn URL"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              />
            </div>

            <div {...getRootProps()} className="cursor-pointer">
              <input {...getInputProps()} />
              <div className={`
                border-2 border-dashed rounded-lg p-6 text-center transition-colors
                ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
              `}>
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600">
                  {resume ? resume.name : 'Drop your resume here, or click to select'}
                </p>
                <p className="mt-1 text-xs text-gray-500">PDF up to 10MB</p>
              </div>
            </div>
          </>
        );

      case 3:
        return (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Heart size={16} className="inline mr-2" />
                Select your interests
              </label>
              <div className="grid grid-cols-2 gap-2">
                {interests.map((interest) => (
                  <button
                    key={interest}
                    type="button"
                    onClick={() => toggleInterest(interest)}
                    className={`
                      p-2 text-sm rounded-lg transition-colors text-left
                      ${selectedInterests.has(interest)
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }
                    `}
                  >
                    {interest}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Briefcase size={16} className="inline mr-2" />
                Companies you're interested in
              </label>
              <div className="grid grid-cols-2 gap-2">
                {companies.map((company) => (
                  <button
                    key={company}
                    type="button"
                    onClick={() => toggleCompany(company)}
                    className={`
                      p-2 text-sm rounded-lg transition-colors text-left
                      ${selectedCompanies.has(company)
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }
                    `}
                  >
                    {company}
                  </button>
                ))}
              </div>
            </div>
          </>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] opacity-40" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-gray-50 to-gray-50" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
          <div className="p-8">
            <div className="flex items-center justify-center mb-8">
              <img
                src="/logo.png"
                alt="Milo"
                className="h-24 w-auto object-contain"
              />
            </div>

            <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
              {isLogin ? 'Welcome back' : step === 1 ? 'Create your account' : step === 2 ? 'Professional details' : 'Your preferences'}
            </h2>
            <p className="text-center text-gray-600 mb-8">
              {isLogin
                ? 'Sign in to continue to Milo'
                : step === 1 ? 'Start your journey with Milo'
                : step === 2 ? 'Help us personalize your experience'
                : 'Almost there! Tell us what you like'}
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <AnimatePresence mode="wait">
                {!isLogin && (
                  <motion.div
                    key={step}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-4"
                  >
                    {renderStep()}
                  </motion.div>
                )}

                {isLogin && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                  >
                    <div className="relative">
                      <Mail
                        size={18}
                        className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                      />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email address"
                        className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                      />
                      <ValidationPopup
                        message={validationMessage}
                        show={validationField === 'email'}
                        onClose={() => setValidationField(null)}
                      />
                    </div>

                    <div className="relative">
                      <Lock
                        size={18}
                        className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                      />
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                      />
                      <ValidationPopup
                        message={validationMessage}
                        show={validationField === 'password'}
                        onClose={() => setValidationField(null)}
                      />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg"
                >
                  {error}
                </motion.div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors relative"
              >
                <span className={loading ? 'invisible' : 'visible'}>
                  {isLogin ? 'Sign In' : step < 3 ? 'Continue' : 'Create Account'}
                </span>
                {loading && (
                  <Loader2
                    size={20}
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-spin"
                  />
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => {
                  setIsLogin(!isLogin);
                  setStep(1);
                }}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium focus:outline-none"
              >
                {isLogin ? "Don't have an account?" : 'Already have an account?'}
              </button>
            </div>
          </div>

          <div className="px-8 py-6 bg-gray-50 border-t border-gray-100">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">Protected by Milo</span>
              <ArrowRight size={16} className="text-gray-400" />
            </div>
          </div>
        </div>

        {!isLogin && (
          <div className="mt-4 flex justify-center gap-2">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className={`
                  w-2 h-2 rounded-full transition-colors
                  ${step === i ? 'bg-blue-600' : 'bg-gray-300'}
                `}
              />
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
}