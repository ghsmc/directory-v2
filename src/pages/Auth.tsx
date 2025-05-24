import React, { useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import AsyncSelect from 'react-select/async';
import { createClient } from '@supabase/supabase-js';
import { useDropzone } from 'react-dropzone';
import {
  Mail, Lock, User, ArrowRight, Loader2, Upload, Linkedin,
  Briefcase, Heart, School2, HelpCircle, ChevronLeft, ChevronRight
} from 'lucide-react';
import { UniversityDropdown } from '../components/UniversityDropdown';
import { ValidationPopup } from '../components/ValidationPopup';

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

/* ---------- Constants --------------------------------------------------- */

enum WizardStep {
  Account      = 1,
  Professional = 2,
  Clarity      = 3,
  Interests    = 4,
  Companies    = 5,
}

const interests = [
  'Accounting', 'Actuarial Science', 'Advertising', 'Aerospace Engineering',
  'Agricultural Technology', 'Applied Mathematics', 'Architecture',
  'Artificial Intelligence Ethics', 'Astrophysics', 'Behavioral Economics',
  'Biochemistry', 'Bioengineering', 'Bioinformatics', 'Biophysics',
  'Blockchain Technology', 'Brand Management', 'Business Analytics',
  'Chemical Engineering', 'Civil Engineering', 'Climate Policy',
  'Cognitive Neuroscience', 'Commercial Aviation', 'Commodities Trading',
  'Computational Biology', 'Computational Linguistics', 'Computer Graphics',
  'Computer Vision', 'Construction Management', 'Corporate Finance',
  'Creative Writing', 'Cybersecurity', 'Data Engineering',
  'Data Journalism', 'Data Science', 'Design Research', 'Digital Marketing',
  'Digital Product Management', 'Ecological Restoration', 'Econometrics',
  'Education Technology', 'Electrical Engineering', 'Energy Markets',
  'Entrepreneurship', 'Environmental Consulting', 'Environmental Law',
  'Film Production', 'Financial Derivatives', 'Financial Planning',
  'Game Development', 'Genetic Counseling', 'Geospatial Analysis',
  'Global Health', 'Hardware Design', 'Health Economics',
  'Healthcare Administration', 'Hospitality Management', 'Human-Computer Interaction',
  'Industrial Design', 'Industrial Engineering', 'Information Security',
  'Interaction Design', 'International Development', 'International Relations',
  'Investment Banking', 'Journalism', 'Labor Economics',
  'Machine Learning Research', 'Marine Biology', 'Marketing Analytics',
  'Materials Science', 'Mechanical Engineering', 'Medical Device Design',
  'Microbiology', 'Mobile Application Development', 'Molecular Biology',
  'Monetary Policy', 'Natural Language Processing', 'Network Engineering',
  'Neuroscience Research', 'Operations Research', 'Optical Engineering',
  'Organizational Psychology', 'Pharmaceutical R&D', 'Photovoltaic Engineering',
  'Policy Analysis', 'Product Design', 'Public Interest Law',
  'Quantitative Trading', 'Real Estate Finance', 'Renewable Energy Finance',
  'Robotics', 'Social Impact Strategy', 'Software Engineering',
  'Supply-Chain Management', 'Technical Writing', 'Theoretical Physics',
  'Urban Planning', 'User Experience Design', 'Venture Capital',
  'Water Resource Engineering'
].sort();

/* ---------- Helpers ----------------------------------------------------- */

type SelectOption = { label: string; value: string };

const loadCompanyOptions = async (input: string): Promise<SelectOption[]> => {
  const companies = [
    'Amazon', 'Apple', 'Anthropic', 'Bridgewater Associates', 'Google',
    'Goldman Sachs', 'JP Morgan', 'Meta', 'Microsoft', 'OpenAI',
    'Stripe', 'Tesla', 'Zillow', 'Netflix', 'Salesforce', 'Adobe',
    'Oracle', 'IBM', 'Intel', 'NVIDIA', 'Uber', 'Airbnb', 'SpaceX',
    'Palantir', 'Coinbase', 'Square', 'Shopify', 'Zoom', 'Slack',
    'Dropbox', 'Pinterest', 'Snapchat', 'TikTok', 'LinkedIn',
    'Twitter', 'Reddit', 'Discord', 'Figma', 'Notion', 'Canva'
  ];
  return companies
    .filter(c => c.toLowerCase().includes(input.toLowerCase()))
    .map(c => ({ label: c, value: c }));
};

/* ---------- Component --------------------------------------------------- */

export function Auth() {
  /* ----- UI state ------------------------------------------------------ */
  const [isLogin, setIsLogin] = useState(true);
  const [step, setStep] = useState<WizardStep>(WizardStep.Account);

  /* ----- Form fields --------------------------------------------------- */
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [university, setUniversity] = useState('');
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [clarity, setClarity] = useState<'yes' | 'no' | null>(null);
  const [targetCompanies, setTargetCompanies] = useState<SelectOption[]>([]);
  const [selectedInterests, setSelectedInterests] = useState<Set<string>>(new Set());
  const [resume, setResume] = useState<File | null>(null);

  /* ----- UX state ------------------------------------------------------ */
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [validationField, setValidationField] = useState<string | null>(null);

  /* ----- File drop ----------------------------------------------------- */
  const onDrop = useCallback((files: File[]) => { 
    if (files.length > 0) {
      setResume(files[0]); 
    }
  }, []);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, 
    accept: { 'application/pdf': ['.pdf'] }, 
    maxFiles: 1
  });

  /* ---------- Validation ---------------------------------------------- */
  const required = (field: string, value: string) => {
    if (!value) {
      setValidationField(field);
      setValidationMessage(`Please enter your ${field}`);
      return false;
    }
    return true;
  };

  /* ---------- Navigation ---------------------------------------------- */
  const goBack = () => {
    if (step > WizardStep.Account) {
      setStep(prev => (prev - 1) as WizardStep);
    }
  };

  const goNext = () => {
    setStep(prev => (prev + 1) as WizardStep);
  };

  /* ---------- Submission ---------------------------------------------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setValidationField(null);
    setValidationMessage('');

    if (isLogin) {
      if (!(required('email', email) && required('password', password))) return;
      setLoading(true);
      try {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
      } catch (err: any) {
        setError(err.message);
      } finally { 
        setLoading(false); 
      }
      return;
    }

    /* Sign-up flow */
    switch (step) {
      case WizardStep.Account:
        if (!(required('name', name) &&
              required('university', university) &&
              required('email', email) &&
              required('password', password))) return;
        goNext();
        break;

      case WizardStep.Professional:
        goNext();
        break;

      case WizardStep.Clarity:
        if (!clarity) {
          setValidationField('clarity'); 
          setValidationMessage('Please select an option'); 
          return;
        }
        goNext();
        break;

      case WizardStep.Interests:
        goNext();
        break;

      case WizardStep.Companies:
        // final submit
        setLoading(true);
        try {
          const { error } = await supabase.auth.signUp({
            email, 
            password,
            options: {
              data: {
                full_name: name, 
                university, 
                linkedin_url: linkedinUrl,
                know_target: clarity === 'yes',
                interests: Array.from(selectedInterests),
                target_companies: targetCompanies.map(c => c.value)
              }
            }
          });
          if (error) throw error;

          if (resume) {
            const { error: uploadError } = await supabase
              .storage.from('resumes')
              .upload(`${email}/resume.pdf`, resume);
            if (uploadError) throw uploadError;
          }
        } catch (err: any) {
          setError(err.message);
        } finally { 
          setLoading(false); 
        }
        break;
    }
  };

  /* ---------- Render logic -------------------------------------------- */

  const dotCount = useMemo(() => {
    return 5; // Now 5 steps visually
  }, []);

  const renderAccountStep = () => (
    <>
      <FieldWrapper 
        icon={<User size={18} />} 
        field="name"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={() => setValidationField(null)}
      >
        <input 
          type="text" 
          value={name} 
          onChange={e => setName(e.target.value)}
          placeholder="Full name" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
        />
      </FieldWrapper>

      <FieldWrapper 
        icon={<School2 size={18} />} 
        field="university"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={() => setValidationField(null)}
      >
        <UniversityDropdown value={university} onChange={setUniversity} />
      </FieldWrapper>

      <FieldWrapper 
        icon={<Mail size={18} />} 
        field="email"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={() => setValidationField(null)}
      >
        <input 
          type="email" 
          value={email} 
          onChange={e => setEmail(e.target.value)}
          placeholder="Email address" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
        />
      </FieldWrapper>

      <FieldWrapper 
        icon={<Lock size={18} />} 
        field="password"
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={() => setValidationField(null)}
      >
        <input 
          type="password" 
          value={password} 
          onChange={e => setPassword(e.target.value)}
          placeholder="Password" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
        />
      </FieldWrapper>
    </>
  );

  const renderProfessionalStep = () => (
    <>
      <FieldWrapper 
        icon={<Linkedin size={18} />} 
        field=""
        validationField={validationField}
        validationMessage={validationMessage}
        onClose={() => setValidationField(null)}
      >
        <input 
          type="url" 
          value={linkedinUrl} 
          onChange={e => setLinkedinUrl(e.target.value)}
          placeholder="LinkedIn URL" 
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
        />
      </FieldWrapper>

      <div {...getRootProps()} className="cursor-pointer">
        <input {...getInputProps()} />
        <div className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors
              ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}>
          <Upload className="mx-auto h-12 w-12 text-gray-400"/>
          <p className="mt-2 text-sm text-gray-600">
            {resume ? resume.name : 'Drop your resume here, or click to select'}
          </p>
          <p className="mt-1 text-xs text-gray-500">PDF up to 10MB</p>
        </div>
      </div>
    </>
  );

  const renderClarityStep = () => (
    <div className="space-y-6">
      <p className="text-center text-gray-700 font-medium">
        Do you already know <em>what</em> you want to do?
      </p>
      <div className="flex justify-center gap-6">
        {(['yes', 'no'] as const).map(opt => (
          <button key={opt}
            type="button"
            onClick={() => setClarity(opt)}
            className={`px-6 py-3 rounded-lg border transition-colors
              ${clarity === opt
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white hover:bg-gray-50 border-gray-300 text-gray-700'
              }`}>
            {opt === 'yes' ? 'Yes' : 'Not yet'}
          </button>
        ))}
      </div>
      {validationField === 'clarity' && (
        <ValidationPopup 
          message={validationMessage} 
          show 
          onClose={() => setValidationField(null)} 
        />
      )}
    </div>
  );

  const renderInterestStep = () => (
    <>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        <Heart size={16} className="inline mr-2" />
        {clarity === 'yes' 
          ? 'What areas are you interested in?' 
          : 'Do you have an idea of any paths you\'re interested in?'
        }
      </label>

      <SearchableInterestGrid
        interests={interests}
        selected={selectedInterests}
        toggle={(int) => setSelectedInterests(prev => {
          const n = new Set(prev); 
          n.has(int) ? n.delete(int) : n.add(int); 
          return n;
        })}
      />
    </>
  );

  const renderCompanyStep = () => (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        <Briefcase size={16} className="inline mr-2"/>
        {clarity === 'yes' 
          ? 'Companies you\'re interested in'
          : 'Are there any companies you find inspiring or interesting?'
        }
      </label>
      <AsyncSelect
        isMulti 
        cacheOptions 
        defaultOptions
        value={targetCompanies}
        loadOptions={loadCompanyOptions}
        onChange={opts => setTargetCompanies(opts as SelectOption[])}
        placeholder="Start typing a company name…"
        styles={{
          control: (base) => ({
            ...base,
            border: '1px solid #d1d5db',
            borderRadius: '0.5rem',
            padding: '0.125rem',
            '&:hover': {
              borderColor: '#9ca3af'
            }
          }),
          menuPortal: (base) => ({
            ...base,
            zIndex: 9999
          })
        }}
        menuPortalTarget={document.body}
      />
      <p className="text-xs text-gray-500 mt-1">
        We'll use this to surface mentors, alumni paths, and open roles.
      </p>
    </div>
  );

  const renderStep = () => {
    switch (step) {
      case WizardStep.Account:      return renderAccountStep();
      case WizardStep.Professional: return renderProfessionalStep();
      case WizardStep.Clarity:      return renderClarityStep();
      case WizardStep.Interests:    return renderInterestStep();
      case WizardStep.Companies:    return renderCompanyStep();
    }
  };

  const stepTitles = {
    [WizardStep.Account]: 'Create your account',
    [WizardStep.Professional]: 'Professional details',
    [WizardStep.Clarity]: 'Career clarity',
    [WizardStep.Interests]: 'Your interests',
    [WizardStep.Companies]: clarity === 'yes' ? 'Dream companies' : 'Companies that inspire you'
  };

  const stepSubtitles = {
    [WizardStep.Account]: 'Start your journey with Milo',
    [WizardStep.Professional]: 'Help us personalize your experience',
    [WizardStep.Clarity]: 'Tell us where you\'re at',
    [WizardStep.Interests]: clarity === 'yes' 
      ? 'Pick topics that align with your goals'
      : 'Pick topics that intrigue you',
    [WizardStep.Companies]: clarity === 'yes'
      ? 'Pick companies you have in mind'
      : 'These help us understand what excites you'
  };

  const canGoNext = () => {
    if (isLogin) return false;
    return step < WizardStep.Companies;
  };

  const canGoBack = () => {
    if (isLogin) return false;
    return step > WizardStep.Account;
  };

  const getButtonText = () => {
    if (isLogin) return 'Sign In';
    if (step < WizardStep.Companies) return 'Continue';
    return 'Create Account';
  };

  /* ---------- JSX ----------------------------------------------------- */

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      {/* background grid + gradient */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)]
            [background-size:16px_16px] opacity-40"/>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-gray-50 to-gray-50"/>
      </div>

      <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden relative">
          <div className="p-8 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-center mb-8">
              <img src="/logo.png" alt="Milo" className="h-24 w-auto object-contain" />
            </div>

            <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
              {isLogin ? 'Welcome back' : stepTitles[step]}
            </h2>

            <p className="text-center text-gray-600 mb-8">
              {isLogin ? 'Sign in to continue to Milo' : stepSubtitles[step]}
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <AnimatePresence mode="wait">
                <motion.div
                  key={`${isLogin}-${step}`}
                  initial={{opacity:0,x:20}} 
                  animate={{opacity:1,x:0}} 
                  exit={{opacity:0,x:-20}}
                  className="space-y-4">
                  {isLogin ? (
                    <>
                      <FieldWrapper 
                        icon={<Mail size={18}/>} 
                        field="email"
                        validationField={validationField}
                        validationMessage={validationMessage}
                        onClose={() => setValidationField(null)}
                      >
                        <input 
                          type="email" 
                          value={email} 
                          onChange={e => setEmail(e.target.value)}
                          placeholder="Email address" 
                          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
                        />
                      </FieldWrapper>
                      <FieldWrapper 
                        icon={<Lock size={18}/>} 
                        field="password"
                        validationField={validationField}
                        validationMessage={validationMessage}
                        onClose={() => setValidationField(null)}
                      >
                        <input 
                          type="password" 
                          value={password} 
                          onChange={e => setPassword(e.target.value)}
                          placeholder="Password" 
                          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" 
                        />
                      </FieldWrapper>
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

          {/* Navigation buttons in bottom corners */}
          {!isLogin && (
            <div className="absolute bottom-4 left-4 right-4 flex justify-between">
              {canGoBack() ? (
                <button
                  type="button"
                  onClick={goBack}
                  className="flex items-center text-sm text-gray-600 hover:text-gray-800 transition-colors bg-white px-3 py-2 rounded-lg shadow-sm border border-gray-200"
                >
                  <ChevronLeft size={16} className="mr-1" />
                  Back
                </button>
              ) : <div />}
              
              {canGoNext() ? (
                <button
                  type="button"
                  onClick={goNext}
                  className="flex items-center text-sm text-blue-600 hover:text-blue-700 transition-colors bg-white px-3 py-2 rounded-lg shadow-sm border border-blue-200"
                >
                  Next
                  <ChevronRight size={16} className="ml-1" />
                </button>
              ) : <div />}
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

/* ---------- Reusable sub-components ----------------------------------- */

function FieldWrapper({children, icon, field, validationField, validationMessage, onClose}: {
  children: React.ReactNode;
  icon: React.ReactNode;
  field: string;
  validationField: string | null;
  validationMessage: string;
  onClose: () => void;
}) {
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

/* Searchable interest grid --------------------------------------------- */
function SearchableInterestGrid({
  interests, selected, toggle
}: {
  interests: string[]; 
  selected: Set<string>; 
  toggle: (i: string) => void;
}) {
  const [query, setQuery] = useState('');
  const filtered = useMemo(
    () => interests.filter(i => i.toLowerCase().includes(query.toLowerCase())),
    [query, interests]
  );

  return (
    <>
      <div className="mb-2 relative">
        <input
          type="text" 
          value={query} 
          onChange={e => setQuery(e.target.value)}
          placeholder="Search interests…" 
          className="w-full pl-3 pr-10 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
        />
        <HelpCircle size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-300"/>
      </div>

      <div className="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto pr-1">
        {filtered.map(int => (
          <button key={int} type="button" onClick={() => toggle(int)}
            className={`p-2 text-sm rounded-lg transition-colors text-left
              ${selected.has(int)
                ? 'bg-blue-100 text-blue-700'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {int}
          </button>
        ))}
      </div>
    </>
  );
}

export default Auth;