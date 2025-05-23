import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart2, Building2, UserCircle2, Settings, Briefcase, Target,
  Star, Mail, MapPin, ChevronDown, ChevronUp, GraduationCap, 
  Brain, Code, Cloud, Database, LineChart, Network, ArrowUpRight,
  Globe, Users, Calendar, Award, BookOpen, Upload, Bell, Link,
  Sparkles, Rocket, Zap, Lightbulb, Cpu, Layers, Gem, Blocks,
  Infinity, Edit3, Bookmark, Clock, CheckCircle2, XCircle, Heart,
  PieChart, TrendingUp, CheckCircle, XCircleIcon, DollarSign,
  School2
} from 'lucide-react';
import { CareerPathFlow } from '../components/CareerPathFlow';
import { SkillsGrid } from '../components/SkillsGrid';
import { NetworkSection } from '../components/NetworkSection';
import { CareerPathSection } from '../components/CareerPathSection';

const skillsData = [
  { name: 'Python', level: 90, trend: 'up', demand: 95, growth: '+15%' },
  { name: 'React', level: 85, trend: 'up', demand: 92, growth: '+12%' },
  { name: 'TypeScript', level: 80, trend: 'up', demand: 90, growth: '+18%' },
  { name: 'Node.js', level: 85, trend: 'up', demand: 88, growth: '+10%' },
  { name: 'AWS', level: 75, trend: 'up', demand: 85, growth: '+8%' },
  { name: 'Machine Learning', level: 70, trend: 'up', demand: 82, growth: '+20%' }
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

const networkConnections = [
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
  },
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
];

export function Profile() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'profile' | 'personal' | 'preferences' | 'career'>('dashboard');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-3xl font-bold">
                YS
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Yale Student
                </h1>
                <div className="mt-2 flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-1 text-gray-600">
                    <School2 size={16} />
                    Yale University
                  </div>
                  <div className="flex items-center gap-1 text-gray-600">
                    <MapPin size={16} />
                    New Haven, CT
                  </div>
                  <div className="flex items-center gap-1 text-gray-600">
                    <Mail size={16} />
                    student@yale.edu
                  </div>
                </div>
                <div className="mt-4 flex gap-2">
                  {['AI/ML', 'Web Development', 'Quantum Computing'].map((interest) => (
                    <span
                      key={interest}
                      className="px-2 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-700"
                    >
                      {interest}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <button
              className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700"
            >
              Edit Profile
            </button>
          </div>

          <div className="mt-8 flex gap-4 border-t border-gray-200 pt-4">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
              { id: 'profile', label: 'Profile', icon: UserCircle2 },
              { id: 'personal', label: 'Personal Info', icon: Settings },
              { id: 'preferences', label: 'Job Preferences', icon: Briefcase },
              { id: 'career', label: 'Career Path', icon: Target }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors
                  ${activeTab === tab.id
                    ? 'bg-gray-200 text-gray-900'
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

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Career Path Section */}
            <CareerPathSection isDark={false} />

            {/* Network Section */}
            <NetworkSection
              isDark={false}
              connections={networkConnections}
            />

            {/* Applications Section */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold flex items-center gap-2 text-gray-900 mb-6">
                  <Target size={20} />
                  Active Applications
                </h2>
                <div className="space-y-4">
                  {recentApplications.map((app, index) => (
                    <div
                      key={index}
                      className="p-4 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <img
                            src={app.logo}
                            alt={app.company}
                            className="w-10 h-10 rounded-lg object-contain bg-white"
                          />
                          <div>
                            <h3 className="font-medium text-gray-900">{app.role}</h3>
                            <p className="text-sm text-gray-600">{app.company}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className={`
                            px-2 py-1 rounded text-xs font-medium
                            ${app.status === 'Offer' ? 'bg-green-100 text-green-700' :
                              app.status === 'Interview' ? 'bg-blue-100 text-blue-700' :
                              app.status === 'Applied' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-red-100 text-red-700'
                            }
                          `}>
                            {app.status}
                          </div>
                          <div className="px-2 py-1 rounded text-xs font-medium bg-emerald-100 text-emerald-700">
                            {app.matchScore}% Match
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-3 text-sm">
                        {app.status === 'Interview' && (
                          <div className="flex items-center gap-2 text-blue-600">
                            <Calendar size={14} />
                            Next: {app.nextStep}
                          </div>
                        )}
                        {app.status === 'Offer' && (
                          <div className="flex items-center gap-2 text-green-600">
                            <DollarSign size={14} />
                            {app.compensation}
                          </div>
                        )}
                        {app.status === 'Rejected' && (
                          <div className="flex items-center gap-2 text-red-600">
                            <XCircle size={14} />
                            {app.feedback}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="space-y-8">
            {/* Basic Info */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Basic Information</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-600">Full Name</label>
                    <p className="mt-1 text-gray-900">Yale Student</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600">Email</label>
                    <p className="mt-1 text-gray-900">student@yale.edu</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600">Location</label>
                    <p className="mt-1 text-gray-900">New Haven, CT</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600">Phone</label>
                    <p className="mt-1 text-gray-900">+1 (203) 555-0123</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Education */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Education</h2>
                <div className="space-y-6">
                  <div className="flex items-start gap-4">
                    <img
                      src="https://img.logo.dev/yale.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ"
                      alt="Yale University"
                      className="w-12 h-12 rounded-lg object-contain bg-white border border-gray-200"
                    />
                    <div>
                      <h3 className="font-medium text-gray-900">Yale University</h3>
                      <p className="text-gray-600">Bachelor of Science in Computer Science</p>
                      <p className="text-gray-500 mt-1">2021 - 2025</p>
                      <div className="mt-2 flex gap-2">
                        <span className="px-2 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-600">
                          GPA: 3.95
                        </span>
                        <span className="px-2 py-1 rounded-lg text-xs font-medium bg-purple-50 text-purple-600">
                          Dean's List
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Skills */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Skills</h2>
                <SkillsGrid skills={skillsData} isDark={false} />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'career' && (
          <div className="space-y-8">
            <CareerPathSection isDark={false} />

            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold flex items-center gap-2 text-gray-900 mb-6">
                  <Target size={20} />
                  Career Goals
                </h2>
                <div className="space-y-4">
                  <div className="p-4 rounded-lg bg-gray-50">
                    <h3 className="font-medium text-gray-900 mb-2">Short-term Goals</h3>
                    <ul className="space-y-2 text-sm text-gray-700">
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        Secure a software engineering internship at a top tech company
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        Complete advanced machine learning coursework
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        Contribute to open-source projects
                      </li>
                    </ul>
                  </div>
                  <div className="p-4 rounded-lg bg-gray-50">
                    <h3 className="font-medium text-gray-900 mb-2">Long-term Goals</h3>
                    <ul className="space-y-2 text-sm text-gray-700">
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                        Lead an engineering team at a tech company
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                        Start a tech startup focused on AI applications
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                        Mentor other developers and contribute to tech education
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold flex items-center gap-2 text-gray-900 mb-6">
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
                      className="px-3 py-1.5 rounded-lg text-sm font-medium bg-gray-100 text-gray-700"
                    >
                      {interest}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}