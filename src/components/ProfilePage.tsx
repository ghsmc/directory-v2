import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { Mail, School, MapPin, Calendar, Award, BookOpen, Upload, Bell, Users, Building2, Briefcase, ChevronRight, Star, FileText, Brain, Search, Link, Globe, Sparkles, Rocket, Target, ChevronDown, ChevronUp, Zap, Lightbulb, Code, LineChart, Network, Microscope, GitBranch, Cpu, Layers, Gem, Blocks, Infinity, Edit3, Bookmark, Clock, CheckCircle2, XCircle, UserCircle2, Settings, Briefcase as Job, GraduationCap, Heart, BarChart2, PieChart, TrendingUp, CheckCircle, XCircle as XCircleIcon, ArrowUpRight, ExternalLink, TrendingDown, DollarSign, Building } from 'lucide-react';
import { EditProfileModal } from './EditProfileModal';
import { ResumeEditor } from './ResumeEditor';
import { JobCard } from './JobCard';
import { MetricsBar } from './MetricsBar';
import { CareerPathFlow } from './CareerPathFlow';
import { NetworkSection } from './NetworkSection';
import { SkillsGrid } from './SkillsGrid';
import { CompaniesSection } from './CompaniesSection';
import { CareerPathSection } from './CareerPathSection';

interface ProfilePageProps {
  isDark: boolean;
  onClose: () => void;
}

const skills = [
  { name: 'Python', trend: 'up', demand: 95, growth: '+15%' },
  { name: 'React', trend: 'up', demand: 92, growth: '+12%' },
  { name: 'TypeScript', trend: 'up', demand: 90, growth: '+18%' },
  { name: 'Node.js', trend: 'up', demand: 88, growth: '+10%' },
  { name: 'AWS', trend: 'up', demand: 85, growth: '+8%' },
  { name: 'Machine Learning', trend: 'up', demand: 82, growth: '+20%' }
];

const recentApplications = [
  {
    company: 'Google',
    role: 'Software Engineer',
    logo: 'https://img.logo.dev/google.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    status: 'Interview',
    date: '2024-03-15',
    stage: 'Technical Interview',
    nextStep: 'System Design Round',
    matchScore: 95
  },
  {
    company: 'Meta',
    role: 'ML Engineer',
    logo: 'https://img.logo.dev/meta.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    status: 'Applied',
    date: '2024-03-12',
    stage: 'Application Review',
    nextStep: 'Initial Screen',
    matchScore: 92
  },
  {
    company: 'Apple',
    role: 'iOS Developer',
    logo: 'https://img.logo.dev/apple.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    status: 'Rejected',
    date: '2024-03-10',
    feedback: 'More iOS experience needed',
    matchScore: 85
  },
  {
    company: 'Amazon',
    role: 'Software Dev Engineer',
    logo: 'https://img.logo.dev/amazon.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    status: 'Offer',
    date: '2024-03-05',
    compensation: '$165K - $185K',
    benefits: ['RSUs', 'Relocation', 'Sign-on bonus'],
    matchScore: 98
  }
];

const recommendedJobs = [
  {
    id: '1',
    companyLogo: "https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
    companyName: "OpenAI",
    jobTitle: "ML Engineer",
    description: "Join our team building the future of AI",
    location: "San Francisco",
    postedDate: "2 days ago",
    salary: "$180K - $250K",
    skills: ["Python", "PyTorch", "ML"],
    metrics: {
      trajectory: 95,
      valuation: "$80B",
      funding: "$11.3B",
      lastRaised: "1.5y ago",
      age: "8 yrs",
      employees: "2,000",
      openJobs: 156
    },
    badges: {
      unicorn: true,
      trueUpRemote200: false
    }
  },
  {
    id: '2',
    companyLogo: "https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
    companyName: "Anthropic",
    jobTitle: "Research Engineer",
    description: "Work on advanced language models",
    location: "Remote",
    postedDate: "1 day ago",
    salary: "$170K - $240K",
    skills: ["Python", "ML", "NLP"],
    metrics: {
      trajectory: 94,
      valuation: "$4.1B",
      funding: "$1.3B",
      lastRaised: "6m ago",
      age: "3 yrs",
      employees: "150",
      openJobs: 45
    },
    badges: {
      unicorn: true,
      trueUpRemote200: true
    }
  }
];

const careerInsights = [
  {
    title: "AI/ML Engineering",
    growth: "+45%",
    trend: "up",
    description: "Strong match with your ML and Python skills",
    companies: ["OpenAI", "Anthropic", "DeepMind"],
    avgSalary: "$180K - $250K"
  },
  {
    title: "Full Stack Development",
    growth: "+28%",
    trend: "up",
    description: "Leverages your React and Node.js expertise",
    companies: ["Stripe", "Vercel", "MongoDB"],
    avgSalary: "$150K - $220K"
  },
  {
    title: "Cloud Architecture",
    growth: "+32%",
    trend: "up",
    description: "Growing demand for AWS knowledge",
    companies: ["Snowflake", "Databricks", "HashiCorp"],
    avgSalary: "$160K - $230K"
  }
];

const networkConnections = {
  following: [
    {
      name: "Sarah Chen",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
      role: "ML Engineer",
      company: "Google",
      companyLogo: "https://img.logo.dev/google.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2020",
      email: "sarah.chen@gmail.com"
    },
    {
      name: "Michael Park",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e",
      role: "Software Engineer",
      company: "Meta",
      companyLogo: "https://img.logo.dev/meta.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2021",
      email: "mpark@meta.com"
    }
  ],
  recommended: [
    {
      name: "Emily Zhang",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80",
      role: "Product Manager",
      company: "Apple",
      companyLogo: "https://img.logo.dev/apple.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2019",
      email: "emily.z@apple.com"
    },
    {
      name: "David Kim",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e",
      role: "Data Scientist",
      company: "OpenAI",
      companyLogo: "https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2022",
      email: "david.kim@openai.com"
    }
  ],
  connections: [
    {
      name: "Alex Rivera",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
      role: "Engineering Manager",
      company: "Microsoft",
      companyLogo: "https://img.logo.dev/microsoft.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2018",
      email: "arivera@microsoft.com"
    },
    {
      name: "Julia Lee",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb",
      role: "Tech Lead",
      company: "Amazon",
      companyLogo: "https://img.logo.dev/amazon.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ",
      yaleClass: "2020",
      email: "julia.lee@amazon.com"
    }
  ]
};

const skillsData = [
  { name: 'Python', level: 90, trend: 'up', demand: 95, growth: '+15%' },
  { name: 'React', level: 85, trend: 'up', demand: 92, growth: '+12%' },
  { name: 'TypeScript', level: 80, trend: 'up', demand: 90, growth: '+18%' },
  { name: 'Node.js', level: 85, trend: 'up', demand: 88, growth: '+10%' },
  { name: 'AWS', level: 75, trend: 'up', demand: 85, growth: '+8%' },
  { name: 'Machine Learning', level: 70, trend: 'up', demand: 82, growth: '+20%' }
];

const followingCompanies = [
  {
    id: '1',
    name: 'xAI',
    logo: 'https://img.logo.dev/xai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Artificial intelligence research',
    valuation: '$45.0B',
    status: 'Private',
    jobCount: 156
  },
  {
    id: '2',
    name: 'Anthropic',
    logo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'AI systems',
    valuation: '$61.5B',
    status: 'Private',
    jobCount: 45
  },
  {
    id: '3',
    name: 'Perplexity AI',
    logo: 'https://img.logo.dev/perplexity.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Conversational AI',
    valuation: '$9.0B',
    status: 'Private',
    jobCount: 28
  },
  {
    id: '4',
    name: 'Mistral AI',
    logo: 'https://img.logo.dev/mistral.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Generative AI models',
    valuation: '$6.2B',
    status: 'Private',
    jobCount: 42
  }
];

const recommendedCompanies = [
  {
    id: '5',
    name: 'Figure',
    logo: 'https://img.logo.dev/figure.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Humanoid robots',
    valuation: '$2.7B',
    status: 'Private',
    jobCount: 89,
    matchScore: 95
  },
  {
    id: '6',
    name: 'Safe Superintelligence',
    logo: 'https://img.logo.dev/ssi.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Safe artificial intelligence',
    valuation: '$5.0B',
    status: 'Private',
    jobCount: 34,
    matchScore: 92
  },
  {
    id: '7',
    name: 'Sierra',
    logo: 'https://img.logo.dev/sierra.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Enterprise AI',
    valuation: '$4.5B',
    status: 'Private',
    jobCount: 67,
    matchScore: 90
  },
  {
    id: '8',
    name: 'The Bot Company',
    logo: 'https://img.logo.dev/thebotcompany.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    description: 'Household robots',
    valuation: '$2.0B',
    status: 'Private',
    jobCount: 45,
    matchScore: 88
  }
];

export function ProfilePage({ isDark, onClose }: ProfilePageProps) {
  const [showResumeEditor, setShowResumeEditor] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'profile' | 'personal' | 'preferences' | 'career' | 'dashboard' | 'companies'>('dashboard');
  const [resume, setResume] = useState<{ file: File; preview: string } | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    onDrop: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setResume({
          file,
          preview: URL.createObjectURL(file)
        });
      }
    }
  });

  const renderDashboardContent = () => {
    return (
      <div className="space-y-8">
        <MetricsBar 
          isDark={isDark}
          metrics={{
            tokensUsed: 8000
          }}
        />

        <div className={`
          rounded-xl border overflow-hidden
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="p-6">
            <h2 className={`text-lg font-semibold mb-6 flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              <Brain size={18} className="text-purple-500" />
              Career Path Insights
            </h2>
            <CareerPathFlow />
          </div>
        </div>

        <div className={`
          rounded-xl border overflow-hidden
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="p-6">
            <h2 className={`text-lg font-semibold mb-6 flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              <Zap size={18} className="text-amber-500" />
              Skills & Market Demand
            </h2>
            <SkillsGrid skills={skillsData} isDark={isDark} />
          </div>
        </div>

        <NetworkSection
          isDark={isDark}
          connections={networkConnections.connections}
        />

        <div className={`
          rounded-xl border overflow-hidden
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="p-6">
            <h2 className={`text-lg font-semibold mb-6 flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              <Target size={18} className="text-blue-500" />
              Active Applications
            </h2>
            <div className="space-y-4">
              {recommendedJobs.map((job) => (
                <JobCard key={job.id} {...job} isDark={isDark} />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return renderDashboardContent();
      case 'companies':
        return (
          <CompaniesSection 
            isDark={isDark}
            following={followingCompanies}
            recommended={recommendedCompanies}
          />
        );
      case 'career':
        return (
          <div className="space-y-8">
            <CareerPathSection isDark={isDark} />

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Target size={20} />
                  Career Goals
                </h2>
                <div className="space-y-4">
                  <div className={`p-4 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-50'}`}>
                    <h3 className={`font-medium mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>Short-term Goals</h3>
                    <ul className={`list-disc list-inside space-y-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                      <li>Secure a software engineering internship at a top tech company</li>
                      <li>Complete advanced machine learning coursework</li>
                      <li>Contribute to open-source projects</li>
                    </ul>
                  </div>
                  <div className={`p-4 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-50'}`}>
                    <h3 className={`font-medium mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>Long-term Goals</h3>
                    <ul className={`list-disc list-inside space-y-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                      <li>Lead an engineering team at a tech company</li>
                      <li>Start a tech startup focused on AI applications</li>
                      <li>Mentor other developers and contribute to tech education</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Heart size={20} />
                  Professional Interests
                </h2>
                <div className="flex flex-wrap gap-2">
                  {[
                    'Artificial Intelligence',
                    'Machine Learning',
                    'Web Development',
                    'Cloud Computing',
                    'Blockchain',
                    'Quantum Computing',
                    'Cybersecurity',
                    'Data Science'
                  ].map((interest) => (
                    <div
                      key={interest}
                      className={`
                        px-3 py-1.5 rounded-lg text-sm font-medium
                        ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                      `}
                    >
                      {interest}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      case 'profile':
        return (
          <div className="space-y-8">
            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className={`text-lg font-semibold flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    <FileText size={20} />
                    Resume
                  </h2>
                  <button
                    onClick={() => setShowResumeEditor(true)}
                    className={`
                      text-sm flex items-center gap-1
                      ${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'}
                    `}
                  >
                    <Edit3 size={14} />
                    Edit
                  </button>
                </div>

                {resume ? (
                  <div className="space-y-4">
                    <div className={`
                      flex items-center gap-3 p-3 rounded-lg
                      ${isDark ? 'bg-gray-700' : 'bg-gray-50'}
                    `}>
                      <div className={`
                        w-10 h-10 rounded-lg flex items-center justify-center
                        ${isDark ? 'bg-gray-600' : 'bg-gray-100'}
                      `}>
                        <FileText size={20} className={isDark ? 'text-gray-300' : 'text-gray-600'} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className={`font-medium truncate ${isDark ? 'text-white' : 'text-gray-900'}`}>
                          {resume.file.name}
                        </div>
                        <div className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                          PDF • {(resume.file.size / 1024 / 1024).toFixed(1)} MB
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div
                    {...getRootProps()}
                    className={`
                      border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors
                      ${isDark
                        ? 'border-gray-700 hover:border-gray-600'
                        : 'border-gray-300 hover:border-gray-400'
                      }
                    `}
                  >
                    <input {...getInputProps()} />
                    <Upload
                      size={24}
                      className={`mx-auto mb-4 ${isDark ? 'text-gray-500' : 'text-gray-400'}`}
                    />
                    <p className={`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                      {isDragActive ? 'Drop your resume here' : 'Upload your resume'}
                    </p>
                    <p className={`text-xs mt-1 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
                      PDF up to 5MB
                    </p>
                  </div>
                )}
              </div>
            </div>

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Zap size={20} />
                  Skills
                </h2>
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <div
                      key={skill.name}
                      className={`
                        px-3 py-1.5 rounded-lg text-sm font-medium
                        ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                      `}
                    >
                      {skill.name}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <GraduationCap size={20} />
                  Education
                </h2>
                <div className="space-y-4">
                  <div>
                    <h3 className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>Yale University</h3>
                    <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Bachelor of Science in Computer Science</p>
                    <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>2021 - 2025</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'personal':
        return (
          <div className="space-y-8">
            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <UserCircle2 size={20} />
                  Personal Information
                </h2>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className={`text-sm font-medium ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Full Name</label>
                      <p className={`mt-1 ${isDark ? 'text-white' : 'text-gray-900'}`}>Yale Student</p>
                    </div>
                    <div>
                      <label className={`text-sm font-medium ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Email</label>
                      <p className={`mt-1 ${isDark ? 'text-white' : 'text-gray-900'}`}>student@yale.edu</p>
                    </div>
                    <div>
                      <label className={`text-sm font-medium ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Location</label>
                      <p className={`mt-1 ${isDark ? 'text-white' : 'text-gray-900'}`}>New Haven, CT</p>
                    </div>
                    <div>
                      <label className={`text-sm font-medium ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Phone</label>
                      <p className={`mt-1 ${isDark ? 'text-white' : 'text-gray-900'}`}>+1 (203) 555-0123</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Globe size={20} />
                  Languages
                </h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className={isDark ? 'text-white' : 'text-gray-900'}>English</span>
                    <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Native</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className={isDark ? 'text-white' : 'text-gray-900'}>Spanish</span>
                    <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Intermediate</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'preferences':
        return (
          <div className="space-y-8">
            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Settings size={20} />
                  Job Preferences
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className={`text-sm font-medium mb-2 ${isDark ?'text-gray-400' : 'text-gray-600'}`}>Desired Roles</h3>
                    <div className="flex flex-wrap gap-2">
                      {['Software Engineer', 'ML Engineer', 'Data Scientist', 'Full Stack Developer'].map((role) => (
                        <div
                          key={role}
                          className={`
                            px-3 py-1.5 rounded-lg text-sm font-medium
                            ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                          `}
                        >
                          {role}
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h3 className={`text-sm font-medium mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Preferred Locations</h3>
                    <div className="flex flex-wrap gap-2">
                      {['New York', 'San Francisco', 'Boston', 'Remote'].map((location) => (
                        <div
                          key={location}
                          className={`
                            px-3 py-1.5 rounded-lg text-sm font-medium
                            ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                          `}
                        >
                          {location}
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h3 className={`text-sm font-medium mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Industry Preferences</h3>
                    <div className="flex flex-wrap gap-2">
                      {['AI/ML', 'FinTech', 'Healthcare', 'EdTech'].map((industry) => (
                        <div
                          key={industry}
                          className={`
                            px-3 py-1.5 rounded-lg text-sm font-medium
                            ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                          `}
                        >
                          {industry}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className={`
              rounded-xl border shadow-sm overflow-hidden
              ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
            `}>
              <div className="p-6">
                <h2 className={`text-lg font-semibold flex items-center gap-2 mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  <Building2 size={20} />
                  Work Environment
                </h2>
                <div className="space-y-4">
                  <div>
                    <h3 className={`text-sm font-medium mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Preferred Work Style</h3>
                    <div className="flex flex-wrap gap-2">
                      {['Remote', 'Hybrid', 'Flexible Hours'].map((style) => (
                        <div
                          key={style}
                          className={`
                            px-3 py-1.5 rounded-lg text-sm font-medium
                            ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                          `}
                        >
                          {style}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <>
      {showResumeEditor ? (
        <ResumeEditor isDark={isDark} onClose={() => setShowResumeEditor(false)} />
      ) : (
        <div className={`min-h-screen overflow-y-auto ${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
          <EditProfileModal
            isOpen={showEditModal}
            onClose={() => setShowEditModal(false)}
            initialData={{
              university: 'Yale University',
              location: 'New Haven, CT',
              email: 'student@yale.edu',
              major: 'Computer Science',
              interests: ['AI/ML', 'Web Development', 'Quantum Computing'],
              languages: [
                { language: 'English', level: 'Native' },
                { language: 'Spanish', level: 'Intermediate' }
              ],
              about: 'Computer Science student passionate about AI and web development.'
            }}
            onSave={() => {}}
          />

          <div className={`${isDark ? 'bg-gray-800' : 'bg-white'} border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
            <div className="max-w-7xl mx-auto px-4 py-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-6">
                  <div className="w-24 h-24 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-3xl font-bold">
                    YS
                  </div>
                  <div>
                    <h1 className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                      Yale Student
                    </h1>
                    <div className="mt-2 flex items-center gap-4 text-sm">
                      <div className={`flex items-center gap-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                        <School size={16} />
                        Yale University
                      </div>
                      <div className={`flex items-center gap-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                        <MapPin size={16} />
                        New Haven, CT
                      </div>
                      <div className={`flex items-center gap-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                        <Mail size={16} />
                        student@yale.edu
                      </div>
                    </div>
                    <div className="mt-4 flex gap-2">
                      {['AI/ML', 'Web Development', 'Quantum Computing'].map((interest) => (
                        <span
                          key={interest}
                          className={`
                            px-2 py-1 rounded-lg text-xs font-medium
                            ${isDark ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'}
                          `}
                        >
                          {interest}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => setShowEditModal(true)}
                  className={`
                    px-4 py-2 rounded-lg text-sm font-medium
                    ${isDark
                      ? 'bg-blue-500 text-white hover:bg-blue-600'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                    }
                  `}
                >
                  Edit Profile
                </button>
              </div>

              <div className="mt-8 flex gap-4 border-t ${isDark ? 'border-gray-700' : 'border-gray-200'} pt-4">
                {[
                  { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
                  { id: 'companies', label: 'Companies', icon: Building },
                  { id: 'profile', label: 'Profile', icon: UserCircle2 },
                  { id: 'personal', label: 'Personal Info', icon: Settings },
                  { id: 'preferences', label: 'Job Preferences', icon: Job },
                  { id: 'career', label: 'Career Path', icon: Target }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors
                      ${activeTab === tab.id
                        ? isDark
                          ? 'bg-gray-700 text-white'
                          : 'bg-gray-200 text-gray-900'
                        : isDark
                          ? 'text-gray-400 hover:text-gray-300 hover:bg-gray-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }
                    `}
                  >
                    {React.createElement(tab.icon, { size: 16 })}
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="max-w-7xl mx-auto px-4 py-8">
            {renderTabContent()}
          </div>
        </div>
      )}
    </>
  );
}