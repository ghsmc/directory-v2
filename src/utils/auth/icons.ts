import {
  Code, Brain, Cloud, Database, LineChart, Network,
  GitBranch, Cpu, Layers, Gem, Blocks, Infinity,
  Building2, DollarSign, Briefcase, GraduationCap,
  Lightbulb, Rocket, Target, Microscope, Zap,
  PieChart, Globe, Users, Calendar, Award, BookOpen,
  Upload, Bell, Link as LinkIcon
} from 'lucide-react';

const iconMap: Record<string, any> = {
  'Software Engineering': Code,
  'Artificial Intelligence': Brain,
  'Cloud Computing': Cloud,
  'Data Engineering': Database,
  'Data Science': LineChart,
  'DevOps': Network,
  'Machine Learning': Brain,
  'Version Control': GitBranch,
  'Hardware Design': Cpu,
  'System Architecture': Layers,
  'Product Management': Gem,
  'Blockchain': Blocks,
  'Quantum Computing': Infinity,
  'Business Analytics': PieChart,
  'Corporate Finance': DollarSign,
  'Investment Banking': Building2,
  'Product Design': Lightbulb,
  'Entrepreneurship': Rocket,
  'Marketing': Target,
  'Research': Microscope,
  'Engineering': Zap,
  'Education': GraduationCap,
  'Healthcare': Award,
  'Global Business': Globe,
  'Human Resources': Users,
  'Project Management': Calendar,
  'Content Creation': BookOpen,
  'Cloud Infrastructure': Upload,
  'Notifications': Bell,
  'Networking': LinkIcon,
  'Career Development': Briefcase
};

export function getInterestIcon(interest: string) {
  // Try to find an exact match
  if (iconMap[interest]) {
    return iconMap[interest];
  }

  // Look for partial matches
  const words = interest.toLowerCase().split(' ');
  for (const word of words) {
    for (const [key, icon] of Object.entries(iconMap)) {
      if (key.toLowerCase().includes(word)) {
        return icon;
      }
    }
  }

  // Default icon if no match found
  return Lightbulb;
}