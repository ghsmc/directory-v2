export const interests = [
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

export const companies = [
  { name: 'Amazon', domain: 'amazon.com' },
  { name: 'Apple', domain: 'apple.com' },
  { name: 'Anthropic', domain: 'anthropic.com' },
  { name: 'Bridgewater Associates', domain: 'bridgewater.com' },
  { name: 'Google', domain: 'google.com' },
  { name: 'Goldman Sachs', domain: 'goldmansachs.com' },
  { name: 'JP Morgan', domain: 'jpmorgan.com' },
  { name: 'Meta', domain: 'meta.com' },
  { name: 'Microsoft', domain: 'microsoft.com' },
  { name: 'OpenAI', domain: 'openai.com' },
  { name: 'Stripe', domain: 'stripe.com' },
  { name: 'Tesla', domain: 'tesla.com' },
  { name: 'Zillow', domain: 'zillow.com' },
  { name: 'Netflix', domain: 'netflix.com' },
  { name: 'Salesforce', domain: 'salesforce.com' },
  { name: 'Adobe', domain: 'adobe.com' },
  { name: 'Oracle', domain: 'oracle.com' },
  { name: 'IBM', domain: 'ibm.com' },
  { name: 'Intel', domain: 'intel.com' },
  { name: 'NVIDIA', domain: 'nvidia.com' },
  { name: 'Uber', domain: 'uber.com' },
  { name: 'Airbnb', domain: 'airbnb.com' },
  { name: 'SpaceX', domain: 'spacex.com' },
  { name: 'Palantir', domain: 'palantir.com' },
  { name: 'Coinbase', domain: 'coinbase.com' },
  { name: 'Square', domain: 'square.com' },
  { name: 'Shopify', domain: 'shopify.com' },
  { name: 'Zoom', domain: 'zoom.us' },
  { name: 'Slack', domain: 'slack.com' },
  { name: 'Dropbox', domain: 'dropbox.com' },
  { name: 'Pinterest', domain: 'pinterest.com' },
  { name: 'Snapchat', domain: 'snap.com' },
  { name: 'TikTok', domain: 'tiktok.com' },
  { name: 'LinkedIn', domain: 'linkedin.com' },
  { name: 'Twitter', domain: 'twitter.com' },
  { name: 'Reddit', domain: 'reddit.com' },
  { name: 'Discord', domain: 'discord.com' },
  { name: 'Figma', domain: 'figma.com' },
  { name: 'Notion', domain: 'notion.so' },
  { name: 'Canva', domain: 'canva.com' }
].sort((a, b) => a.name.localeCompare(b.name));

export const dummyResumeData = {
  name: 'Raymond Hou',
  contact: {
    email: 'raymond.hou@email.com',
    phone: '(555) 123-4567',
    location: 'San Francisco, CA',
    linkedin: 'linkedin.com/in/raymondhou'
  },
  education: [
    {
      institution: 'Stanford University',
      degree: 'Bachelor of Science in Computer Science',
      dates: 'Sep 2020 - Jun 2024',
      gpa: '3.8/4.0'
    }
  ],
  experience: [
    {
      company: 'Google',
      title: 'Software Engineering Intern',
      dates: 'Jun 2023 - Aug 2023',
      description: 'Developed machine learning models for search ranking, improving click-through rates by 15%. Collaborated with cross-functional teams to implement A/B testing frameworks.'
    },
    {
      company: 'Startup XYZ',
      title: 'Full Stack Developer',
      dates: 'Jan 2023 - May 2023',
      description: 'Built and deployed web applications using React and Node.js. Designed database schemas and implemented RESTful APIs serving 10k+ daily active users.'
    }
  ]
};