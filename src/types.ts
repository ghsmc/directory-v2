export interface Experience {
  company: string;
  companyLogo: string;
  role: string;
  duration: string;
  location: string;
  description: string;
}

export interface Education {
  school: string;
  degree: string;
  field: string;
  year: string;
  gpa?: string;
}

export interface Person {
  id: string;
  name: string;
  avatar: string;
  currentRole: string;
  currentCompany: string;
  companyLogo: string;
  schoolLogo: string;
  location: string;
  bio: string;
  experience: Experience[];
  education: Education[];
  skills: string[];
  email: string;
  matchScore: number;
}