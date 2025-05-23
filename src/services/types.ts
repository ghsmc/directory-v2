export type Category = 'jobs' | 'research' | 'clubs' | 'courses';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  isComplete?: boolean;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  remote: boolean;
  description: string;
  requirements: string[];
  categories: string[];
  salary: string;
  applicationDeadline: string;
  postedDate: string;
  skills: string[];
  employmentType: string;
  experienceLevel: string;
  logoUrl: string;
}

export interface Research {
  id: string;
  title: string;
  institution: string;
  department: string;
  professor: string;
  location: string;
  remote: boolean;
  description: string;
  requirements: string[];
  categories: string[];
  compensation: string;
  applicationDeadline: string;
  duration: string;
  postedDate: string;
  skills: string[];
  logoUrl: string;
}

export interface Club {
  id: string;
  name: string;
  university: string;
  category: string;
  description: string;
  meetingSchedule: string;
  location: string;
  membershipRequirements: string;
  leadershipOpportunities: string[];
  activities: string[];
  contactEmail: string;
  socialMedia: {
    instagram?: string;
    discord?: string;
    website?: string;
    twitter?: string;
    facebook?: string;
    linkedin?: string;
  };
  tags: string[];
  logoUrl: string;
}

export interface Course {
  id: string;
  code: string;
  title: string;
  department: string;
  school: string;
  professor: string;
  term: string;
  schedule: string;
  location: string;
  credits: number;
  description: string;
  prerequisites: string;
  syllabus: string;
  enrollmentCapacity: number;
  currentEnrollment: number;
  waitlist: number;
  evaluationScore: number;
  evaluationComments: string[];
  tags: string[];
  logoUrl: string;
}