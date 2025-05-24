export enum WizardStep {
  Account = 1,
  Professional = 2,
  ResumeReview = 3,
  Clarity = 4,
  Interests = 5,
  Companies = 6,
}

export interface ContactInfo {
  email: string;
  phone: string;
  location: string;
  linkedin: string;
}

export interface Education {
  institution: string;
  degree: string;
  dates: string;
  gpa: string;
}

export interface Experience {
  company: string;
  title: string;
  dates: string;
  description: string;
}

export interface ResumeData {
  name: string;
  contact: ContactInfo;
  education: Education[];
  experience: Experience[];
}

export interface AuthFormData {
  email: string;
  password: string;
  name: string;
  university: string;
  linkedinUrl: string;
  clarity: 'yes' | 'no' | null;
  selectedCompanies: Set<string>;
  selectedInterests: Set<string>;
  resume: File | null;
  resumeData: ResumeData;
} 