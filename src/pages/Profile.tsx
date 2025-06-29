import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { Navbar } from '../components/Navbar';
import { FileText, Upload, RefreshCw, Target, Calendar, DollarSign, XCircle } from 'lucide-react';
import { SkillsGrid } from '../components/SkillsGrid';
import { NetworkSection } from '../components/NetworkSection';
import { CareerPathSection } from '../components/CareerPathSection';

const skillsData = [
  { name: 'Python', level: 90, trend: 'up' as const, demand: 95, growth: '+15%' },
  { name: 'React', level: 85, trend: 'up' as const, demand: 92, growth: '+12%' },
  { name: 'TypeScript', level: 80, trend: 'up' as const, demand: 90, growth: '+18%' },
  { name: 'Node.js', level: 85, trend: 'up' as const, demand: 88, growth: '+10%' },
  { name: 'AWS', level: 75, trend: 'up' as const, demand: 85, growth: '+8%' },
  { name: 'Machine Learning', level: 70, trend: 'up' as const, demand: 82, growth: '+20%' }
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

const initialProfile = {
  personal_info: {
    name: 'Raymond Hou',
    email: 'rayconghou@gmail.com',
    phone: '334-467-7669',
    location: '',
    linkedin: 'Linkedin',
    github: 'Github',
  },
  work_experience: [
    {
      company: 'Fortune Collective',
      position: 'CTO',
      date_range: 'January 2025 – Present',
      description: [
        'CTO of all-in-one crypto retail mobile hub generating 6-figure monthly revenue. Built Maneki, an LLM-powered AI agent personally guiding users through portfolio analysis, custom index creation, and social investing.',
        'Integrated seamless cross-platform architecture with a Node.js backend, PostgreSQL for transaction logging, and Firebase for real-time updates, enabling Apple Pay crypto purchases, DeFi integrations, and NLP-based sentiment analysis and market trend detection.'
      ],
      location: 'Remote',
    },
    {
      company: 'Yale University',
      position: 'Sensors Research Assistant',
      date_range: 'September 2024 – Present',
      description: [
        "Building CAFFEINE (Collaborative and Affordable Framework For Experiments in Interactive Networked Electronics), an open-source hardware/software framework enabling real-time, low-latency sonification of sensor data from wearable embedded systems, research paper accepted by ICMC '25.",
        'Implemented a many-to-many network topology in Arduino utilizing UDP protocols that allow for unlimited ESP32-powered pods and clients, only constrained by hardware capacity.'
      ],
      location: 'New Haven, CT',
    },
    {
      company: 'Yale University',
      position: 'Computer Society Software Developer',
      date_range: 'September 2023 – September 2024',
      description: [
        'Developed Yale Butteries, a mobile food-ordering app serving 14 college-wide butteries (late-night snack shops), enhancing ordering efficiency by 10 minutes for over 4,000 students with real-time order updates.',
        'Built VibeSync from scratch, integrating Spotify API for personalized music experiences in the backend and leveraging Tailwind CSS to enhance app responsiveness and design.'
      ],
      location: 'New Haven, CT',
    }
  ],
  education: [
    {
      institution: 'Yale University',
      degree: 'B.S. in Computer Science',
      graduation_date: 'Expected Graduation May 2027',
      gpa: '3.8',
      location: 'New Haven, CT',
      details: [
        'Relevant Coursework: Systems Programming, Computer Organization, Data Structures, Algorithms, Machine Learning, Deep Learning Theory and Applications, Computational Intelligence for Games, Discrete Mathematics, Linear Algebra, Multi-variable Calculus'
      ]
    }
  ],
  skills: [
    'Python', 'C/C++', 'Java', 'Javascript', 'Typescript', 'SQL', 'HTML', 'CSS/Tailwind', 'Racket', 'React', 'Node.js', 'Express.js', 'Spring Boot', 'Flask', 'RestAPI', 'Pandas', 'NumPy', 'Selenium', 'Scikit', 'Git', 'Docker', 'VSCode', 'Vercel', 'Prisma'
  ],
  extracted_keywords: [
    'Crypto', 'AI', 'Node.js', 'PostgreSQL', 'Firebase', 'Arduino', 'UDP', 'ESP32', 'Spotify API', 'Tailwind CSS', 'LLM', 'IRIS Intersystems', 'CAS Authentication', 'CNN', 'Google Maps', 'Geocoding APIs'
  ],
  summary: ''
};

type PersonalInfoKey = keyof typeof initialProfile.personal_info;
type WorkExperience = typeof initialProfile.work_experience[number];
type Education = typeof initialProfile.education[number];

export default function ProfilePage() {
  const [profile, setProfile] = useState<typeof initialProfile>(initialProfile);
  const [editing, setEditing] = useState(false);
  const [activeTab, setActiveTab] = useState<'personal' | 'applications'>('personal');
  const [resume, setResume] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const [newSkill, setNewSkill] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: useCallback((acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        setResume(acceptedFiles[0]);
        handleResumeUpload(acceptedFiles[0]);
      }
    }, []),
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  const handleResumeUpload = async (file: File) => {
    setIsUploading(true);
    setUploadMessage('Uploading and parsing resume...');
    
    try {
      const formData = new FormData();
      formData.append('resume', file);
      
      const response = await fetch('http://localhost:8000/api/resume/parse', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to parse resume');
      }
      
      const parsedData = await response.json();
      
      // Update profile with parsed data
      setProfile(prev => ({
        ...prev,
        personal_info: { ...prev.personal_info, ...parsedData.personal_info },
        work_experience: parsedData.work_experience || prev.work_experience,
        education: parsedData.education || prev.education,
        skills: parsedData.skills || prev.skills,
        extracted_keywords: parsedData.extracted_keywords || prev.extracted_keywords,
        summary: parsedData.summary || prev.summary
      }));
      
      setUploadMessage('Resume parsed successfully! Your profile has been updated.');
      setTimeout(() => setUploadMessage(''), 3000);
      
    } catch (error) {
      console.error('Error uploading resume:', error);
      setUploadMessage('Error parsing resume. Please try again.');
      setTimeout(() => setUploadMessage(''), 3000);
    } finally {
      setIsUploading(false);
    }
  };

  // Handlers for editing fields
  const handlePersonalChange = (field: PersonalInfoKey, value: string) => {
    setProfile((prev) => ({
      ...prev,
      personal_info: { ...prev.personal_info, [field]: value },
    }));
  };

  const handleWorkChange = (idx: number, field: keyof WorkExperience, value: any) => {
    setProfile((prev) => {
      const work = [...prev.work_experience];
      work[idx] = { ...work[idx], [field]: value };
      return { ...prev, work_experience: work };
    });
  };

  const handleEducationChange = (idx: number, field: keyof Education, value: any) => {
    setProfile((prev) => {
      const edu = [...prev.education];
      edu[idx] = { ...edu[idx], [field]: value };
      return { ...prev, education: edu };
    });
  };

  const handleSkillChange = (idx: number, value: string) => {
    setProfile((prev) => {
      const skills = [...prev.skills];
      skills[idx] = value;
      return { ...prev, skills };
    });
  };

  const addSkill = () => setProfile((prev) => ({ ...prev, skills: [...prev.skills, ''] }));
  const removeSkill = (idx: number) => setProfile((prev) => {
    const skills = [...prev.skills];
    skills.splice(idx, 1);
    return { ...prev, skills };
  });

  const renderPersonalInfoContent = () => (
    <div className="relative">
      {/* Resume Upload Section */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold flex items-center gap-2 text-gray-900">
              <FileText size={20} />
              Resume
            </h2>
          </div>
          
          {uploadMessage && (
            <div className={`mb-4 p-3 rounded-lg text-sm ${
              uploadMessage.includes('Error') 
                ? 'bg-red-50 text-red-700' 
                : 'bg-green-50 text-green-700'
            }`}>
              {uploadMessage}
            </div>
          )}
          
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors
              ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
            `}
          >
            <input {...getInputProps()} />
            {isUploading ? (
              <div className="flex items-center justify-center gap-2">
                <RefreshCw size={24} className="animate-spin text-blue-600" />
                <span className="text-blue-600">Processing resume...</span>
              </div>
            ) : (
              <>
                <Upload size={24} className="mx-auto mb-4 text-gray-400" />
                <p className="text-sm font-medium text-gray-700">
                  {resume ? resume.name : 'Upload your resume to update your profile'}
                </p>
                <p className="text-xs mt-1 text-gray-500">
                  PDF up to 10MB • AI will automatically parse and update your information
                </p>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Personal Information */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-900">Personal Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(profile.personal_info).map(([key, value]) => (
              <div key={key}>
                <label className="block text-sm text-gray-600 capitalize mb-1">{key}</label>
                <input
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={value}
                  disabled={!editing}
                  onChange={e => handlePersonalChange(key as PersonalInfoKey, e.target.value)}
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Skills */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-900">Skills</h2>
          {editing ? (
            <div>
              <div className="flex flex-wrap gap-2 mb-2">
                {profile.skills.map((skill, idx) => (
                  <div
                    key={idx}
                    className="flex items-center bg-blue-100 text-blue-700 rounded-full px-3 py-1 text-sm font-medium transition-colors hover:bg-blue-200"
                  >
                    <span>{skill}</span>
                    <button
                      onClick={() => removeSkill(idx)}
                      className="ml-1 text-blue-500"
                      aria-label={`Remove ${skill}`}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
              <input
                type="text"
                className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-md"
                placeholder="Add a skill and press Enter"
                value={newSkill}
                onChange={e => setNewSkill(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter' && newSkill.trim()) {
                    if (!profile.skills.includes(newSkill.trim())) {
                      setProfile(prev => ({ ...prev, skills: [...prev.skills, newSkill.trim()] }));
                    }
                    setNewSkill('');
                  }
                }}
              />
            </div>
          ) : (
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="bg-gray-100 text-gray-700 rounded-full px-3 py-1 text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Work Experience */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-900">Work Experience</h2>
          <div className="space-y-6">
            {profile.work_experience.map((exp, idx) => (
              <div key={idx} className="border-b border-gray-100 pb-4 last:border-b-0">
                <div className="flex gap-2 mb-2">
                  {editing ? (
                    <input
                      className="font-semibold text-gray-800 text-base border-b border-gray-200 focus:ring-blue-500 focus:outline-none flex-1 min-w-[180px]"
                      value={exp.position}
                      onChange={e => handleWorkChange(idx, 'position', e.target.value)}
                    />
                  ) : (
                    <span className="font-semibold text-gray-800 text-base inline-block">{exp.position}</span>
                  )}
                  <span className="text-gray-400">@</span>
                  {editing ? (
                    <input
                      className="font-semibold text-blue-700 text-base border-b border-gray-200 focus:ring-blue-500 focus:outline-none flex-shrink-0 w-48"
                      value={exp.company}
                      onChange={e => handleWorkChange(idx, 'company', e.target.value)}
                    />
                  ) : (
                    <span className="font-semibold text-blue-700 text-base inline-block">{exp.company}</span>
                  )}
                </div>
                <div className="text-sm text-gray-500 mb-2 flex gap-2 flex-wrap">
                  {editing ? (
                    <input
                      className="border-b border-gray-200 focus:ring-blue-500 focus:outline-none"
                      value={exp.date_range}
                      onChange={e => handleWorkChange(idx, 'date_range', e.target.value)}
                    />
                  ) : (
                    <span className="inline-block">{exp.date_range}</span>
                  )}
                  {', '}
                  {editing ? (
                    <input
                      className="border-b border-gray-200 focus:ring-blue-500 focus:outline-none"
                      value={exp.location}
                      onChange={e => handleWorkChange(idx, 'location', e.target.value)}
                    />
                  ) : (
                    <span className="inline-block">{exp.location}</span>
                  )}
                </div>
                <ul className="list-disc ml-6 text-gray-700 text-sm space-y-1">
                  {exp.description.map((desc, dIdx) => (
                    <li key={dIdx}>
                      {editing ? (
                        <textarea
                          className="w-full border-b border-gray-100 focus:ring-blue-500 focus:outline-none resize-none"
                          rows={2}
                          value={desc}
                          onChange={e => {
                            const newDesc = [...exp.description];
                            newDesc[dIdx] = e.target.value;
                            handleWorkChange(idx, 'description', newDesc);
                          }}
                        />
                      ) : (
                        <div className="w-full text-gray-700 text-sm whitespace-pre-line break-words">{desc}</div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Education */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-900">Education</h2>
          <div className="space-y-6">
            {profile.education.map((edu, idx) => (
              <div key={idx} className="border-b border-gray-100 pb-4 last:border-b-0">
                <div className="flex gap-2 mb-2">
                  {editing ? (
                    <input
                      className="font-semibold text-gray-800 text-base border-b border-gray-200 focus:ring-blue-500 focus:outline-none flex-1 min-w-[180px]"
                      value={edu.degree}
                      onChange={e => handleEducationChange(idx, 'degree', e.target.value)}
                    />
                  ) : (
                    <span className="font-semibold text-gray-800 text-base inline-block">{edu.degree}</span>
                  )}
                  <span className="text-gray-400">@</span>
                  {editing ? (
                    <input
                      className="font-semibold text-blue-700 text-base border-b border-gray-200 focus:ring-blue-500 focus:outline-none flex-shrink-0 w-48"
                      value={edu.institution}
                      onChange={e => handleEducationChange(idx, 'institution', e.target.value)}
                    />
                  ) : (
                    <span className="font-semibold text-blue-700 text-base inline-block">{edu.institution}</span>
                  )}
                </div>
                <div className="text-sm text-gray-500 mb-2 flex gap-2 flex-wrap">
                  {editing ? (
                    <input
                      className="border-b border-gray-200 focus:ring-blue-500 focus:outline-none"
                      value={edu.graduation_date}
                      onChange={e => handleEducationChange(idx, 'graduation_date', e.target.value)}
                    />
                  ) : (
                    <span className="inline-block">{edu.graduation_date}</span>
                  )}
                  {', '}
                  {editing ? (
                    <input
                      className="border-b border-gray-200 focus:ring-blue-500 focus:outline-none"
                      value={edu.location}
                      onChange={e => handleEducationChange(idx, 'location', e.target.value)}
                    />
                  ) : (
                    <span className="inline-block">{edu.location}</span>
                  )}
                  {', GPA: '}
                  {editing ? (
                    <input
                      className="border-b border-gray-200 focus:ring-blue-500 focus:outline-none w-12"
                      value={edu.gpa}
                      onChange={e => handleEducationChange(idx, 'gpa', e.target.value)}
                    />
                  ) : (
                    <span className="inline-block">{edu.gpa}</span>
                  )}
                </div>
                <ul className="list-disc ml-6 text-gray-700 text-sm space-y-1">
                  {edu.details.map((detail, dIdx) => (
                    <li key={dIdx}>
                      {editing ? (
                        <textarea
                          className="w-full border-b border-gray-100 focus:ring-blue-500 focus:outline-none resize-none"
                          rows={2}
                          value={detail}
                          onChange={e => {
                            const newDetails = [...edu.details];
                            newDetails[dIdx] = e.target.value;
                            handleEducationChange(idx, 'details', newDetails);
                          }}
                        />
                      ) : (
                        <div className="w-full text-gray-700 text-sm whitespace-pre-line break-words">{detail}</div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderApplicationsContent = () => (
    <div className="space-y-6">
      <CareerPathSection isDark={false} />
      <NetworkSection isDark={false} connections={networkConnections} />
      
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
      
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Skills Overview</h2>
          <SkillsGrid skills={skillsData} isDark={false} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px] flex flex-col">
        {/* Fixed Header */}
        <div className="fixed top-0 inset-x-0 z-40 bg-white border-b border-gray-200 md:left-[72px]">
          <div className="max-w-2xl mx-auto px-4">
            <div className="flex items-center justify-center h-[72px]">
              <div className="flex items-center gap-8">
                <button
                  onClick={() => setActiveTab('personal')}
                  className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                    activeTab === 'personal' ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Personal Info
                  {activeTab === 'personal' && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
                      initial={false}
                    />
                  )}
                </button>
                <button
                  onClick={() => setActiveTab('applications')}
                  className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                    activeTab === 'applications' ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Applications
                  {activeTab === 'applications' && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
                      initial={false}
                    />
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto pt-[72px]">
          <div className="max-w-2xl mx-auto px-4 pb-24">
            <div className="pt-4">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  {activeTab === 'personal' ? renderPersonalInfoContent() : renderApplicationsContent()}
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
      {/* Floating Edit/Done Button */}
      <div className="fixed bottom-8 right-8 z-50">
        <button
          onClick={() => setEditing((e) => !e)}
          className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold shadow-lg hover:bg-blue-700 transition-colors"
        >
          {editing ? 'Done' : 'Edit'}
        </button>
      </div>
    </div>
  );
} 