import { Person } from '../types';

export const mockPeople: Person[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    currentRole: 'Senior ML Engineer',
    currentCompany: 'OpenAI',
    companyLogo: 'https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/stanford.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'ML engineer focused on large language models and AI safety.',
    experience: [
      {
        company: 'OpenAI',
        companyLogo: 'https://img.logo.dev/openai.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Senior ML Engineer',
        duration: '2022 - Present',
        location: 'San Francisco, CA',
        description: 'Working on large language models and AI safety research.'
      },
      {
        company: 'Google',
        companyLogo: 'https://img.logo.dev/google.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2020 - 2022',
        location: 'Mountain View, CA',
        description: 'Developed recommendation systems for Google Search.'
      }
    ],
    education: [
      {
        school: 'Stanford University',
        degree: 'MS',
        field: 'Computer Science',
        year: '2020',
        gpa: '3.95'
      }
    ],
    skills: ['Python', 'PyTorch', 'ML'],
    email: 'sarah.chen@example.com',
    matchScore: 95
  },
  {
    id: '2',
    name: 'Michael Park',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e',
    currentRole: 'AI Research Scientist',
    currentCompany: 'Anthropic',
    companyLogo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/mit.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'AI researcher specializing in reinforcement learning.',
    experience: [
      {
        company: 'Anthropic',
        companyLogo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'AI Research Scientist',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Leading research in AI alignment and safety.'
      },
      {
        company: 'DeepMind',
        companyLogo: 'https://img.logo.dev/deepmind.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Research Engineer',
        duration: '2021 - 2023',
        location: 'London, UK',
        description: 'Worked on reinforcement learning systems.'
      }
    ],
    education: [
      {
        school: 'MIT',
        degree: 'PhD',
        field: 'Computer Science',
        year: '2021'
      }
    ],
    skills: ['Python', 'JAX', 'RL'],
    email: 'michael.park@example.com',
    matchScore: 92
  },
  {
    id: '3',
    name: 'Emily Zhang',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
    currentRole: 'Software Engineer',
    currentCompany: 'Stripe',
    companyLogo: 'https://img.logo.dev/stripe.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/berkeley.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'New York, NY',
    bio: 'Full-stack engineer focused on payments infrastructure.',
    experience: [
      {
        company: 'Stripe',
        companyLogo: 'https://img.logo.dev/stripe.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Software Engineer',
        duration: '2022 - Present',
        location: 'New York, NY',
        description: 'Building next-gen payments infrastructure.'
      },
      {
        company: 'Meta',
        companyLogo: 'https://img.logo.dev/meta.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Software Engineer',
        duration: '2020 - 2022',
        location: 'Seattle, WA',
        description: 'Worked on React Native infrastructure.'
      }
    ],
    education: [
      {
        school: 'UC Berkeley',
        degree: 'BS',
        field: 'EECS',
        year: '2020'
      }
    ],
    skills: ['TypeScript', 'React', 'Go'],
    email: 'emily.zhang@example.com',
    matchScore: 88
  },
  {
    id: '4',
    name: 'Alex Rivera',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    currentRole: 'Product Engineer',
    currentCompany: 'Vercel',
    companyLogo: 'https://img.logo.dev/vercel.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/cmu.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'Remote',
    bio: 'Full-stack developer specializing in React and Next.js.',
    experience: [
      {
        company: 'Vercel',
        companyLogo: 'https://img.logo.dev/vercel.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Product Engineer',
        duration: '2023 - Present',
        location: 'Remote',
        description: 'Building the future of web development.'
      },
      {
        company: 'Shopify',
        companyLogo: 'https://img.logo.dev/shopify.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Senior Developer',
        duration: '2021 - 2023',
        location: 'Remote',
        description: 'Led frontend infrastructure team.'
      }
    ],
    education: [
      {
        school: 'Carnegie Mellon',
        degree: 'MS',
        field: 'Software Engineering',
        year: '2021'
      }
    ],
    skills: ['Next.js', 'React', 'Node.js'],
    email: 'alex.rivera@example.com',
    matchScore: 90
  },
  {
    id: '5',
    name: 'Julia Lee',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80',
    currentRole: 'ML Platform Engineer',
    currentCompany: 'Databricks',
    companyLogo: 'https://img.logo.dev/databricks.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/yale.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building scalable ML infrastructure and tools.',
    experience: [
      {
        company: 'Databricks',
        companyLogo: 'https://img.logo.dev/databricks.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Platform Engineer',
        duration: '2022 - Present',
        location: 'San Francisco, CA',
        description: 'Leading ML infrastructure development.'
      },
      {
        company: 'Amazon',
        companyLogo: 'https://img.logo.dev/amazon.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Software Engineer',
        duration: '2020 - 2022',
        location: 'Seattle, WA',
        description: 'Worked on AWS SageMaker.'
      }
    ],
    education: [
      {
        school: 'Yale University',
        degree: 'BS',
        field: 'Computer Science',
        year: '2020'
      }
    ],
    skills: ['Python', 'Spark', 'MLOps'],
    email: 'julia.lee@example.com',
    matchScore: 87
  },
  {
    id: '6',
    name: 'David Kim',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    currentRole: 'Research Engineer',
    currentCompany: 'DeepMind',
    companyLogo: 'https://img.logo.dev/deepmind.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/oxford.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'London, UK',
    bio: 'Researching reinforcement learning and robotics.',
    experience: [
      {
        company: 'DeepMind',
        companyLogo: 'https://img.logo.dev/deepmind.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Research Engineer',
        duration: '2023 - Present',
        location: 'London, UK',
        description: 'Working on robotics and RL.'
      }
    ],
    education: [
      {
        school: 'Oxford University',
        degree: 'PhD',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'PyTorch', 'RL'],
    email: 'david.kim@example.com',
    matchScore: 89
  },
  {
    id: '7',
    name: 'Rachel Chen',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2',
    currentRole: 'Frontend Engineer',
    currentCompany: 'Figma',
    companyLogo: 'https://img.logo.dev/figma.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/ucla.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building design tools and creative software.',
    experience: [
      {
        company: 'Figma',
        companyLogo: 'https://img.logo.dev/figma.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Frontend Engineer',
        duration: '2022 - Present',
        location: 'San Francisco, CA',
        description: 'Developing core design platform features.'
      }
    ],
    education: [
      {
        school: 'UCLA',
        degree: 'BS',
        field: 'Computer Science',
        year: '2022'
      }
    ],
    skills: ['TypeScript', 'React', 'WebGL'],
    email: 'rachel.chen@example.com',
    matchScore: 86
  },
  {
    id: '8',
    name: 'Thomas Wilson',
    avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
    currentRole: 'AI Safety Researcher',
    currentCompany: 'Anthropic',
    companyLogo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/harvard.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Working on AI alignment and safety research.',
    experience: [
      {
        company: 'Anthropic',
        companyLogo: 'https://img.logo.dev/anthropic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'AI Safety Researcher',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Developing safe and aligned AI systems.'
      }
    ],
    education: [
      {
        school: 'Harvard University',
        degree: 'PhD',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'AI Safety'],
    email: 'thomas.wilson@example.com',
    matchScore: 91
  },
  {
    id: '9',
    name: 'Sophie Anderson',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    currentRole: 'ML Engineer',
    currentCompany: 'Scale AI',
    companyLogo: 'https://img.logo.dev/scale.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/caltech.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building ML infrastructure and tools.',
    experience: [
      {
        company: 'Scale AI',
        companyLogo: 'https://img.logo.dev/scale.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2022 - Present',
        location: 'San Francisco, CA',
        description: 'Developing ML infrastructure and tools.'
      }
    ],
    education: [
      {
        school: 'Caltech',
        degree: 'BS',
        field: 'Computer Science',
        year: '2022'
      }
    ],
    skills: ['Python', 'ML', 'MLOps'],
    email: 'sophie.anderson@example.com',
    matchScore: 88
  },
  {
    id: '10',
    name: 'James Taylor',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    currentRole: 'Research Scientist',
    currentCompany: 'Cohere',
    companyLogo: 'https://img.logo.dev/cohere.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/princeton.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'Toronto, Canada',
    bio: 'Developing large language models.',
    experience: [
      {
        company: 'Cohere',
        companyLogo: 'https://img.logo.dev/cohere.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Research Scientist',
        duration: '2023 - Present',
        location: 'Toronto, Canada',
        description: 'Working on large language models.'
      }
    ],
    education: [
      {
        school: 'Princeton University',
        degree: 'PhD',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'NLP', 'ML'],
    email: 'james.taylor@example.com',
    matchScore: 87
  },
  {
    id: '11',
    name: 'Emma Davis',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
    currentRole: 'AI Engineer',
    currentCompany: 'Adept AI',
    companyLogo: 'https://img.logo.dev/adept.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/columbia.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building AI agents and automation systems.',
    experience: [
      {
        company: 'Adept AI',
        companyLogo: 'https://img.logo.dev/adept.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'AI Engineer',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Developing AI agents for automation.'
      }
    ],
    education: [
      {
        school: 'Columbia University',
        degree: 'MS',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'Robotics'],
    email: 'emma.davis@example.com',
    matchScore: 86
  },
  {
    id: '12',
    name: 'Daniel Lee',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    currentRole: 'AI Researcher',
    currentCompany: 'Character AI',
    companyLogo: 'https://img.logo.dev/character.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/cornell.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'Palo Alto, CA',
    bio: 'Developing conversational AI systems.',
    experience: [
      {
        company: 'Character AI',
        companyLogo: 'https://img.logo.dev/character.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'AI Researcher',
        duration: '2023 - Present',
        location: 'Palo Alto, CA',
        description: 'Building conversational AI characters.'
      }
    ],
    education: [
      {
        school: 'Cornell University',
        degree: 'PhD',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'NLP', 'ML'],
    email: 'daniel.lee@example.com',
    matchScore: 85
  },
  {
    id: '13',
    name: 'Olivia Wang',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    currentRole: 'ML Engineer',
    currentCompany: 'Inflection AI',
    companyLogo: 'https://img.logo.dev/inflection.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/upenn.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'Palo Alto, CA',
    bio: 'Working on personal AI assistants.',
    experience: [
      {
        company: 'Inflection AI',
        companyLogo: 'https://img.logo.dev/inflection.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2023 - Present',
        location: 'Palo Alto, CA',
        description: 'Developing personal AI assistants.'
      }
    ],
    education: [
      {
        school: 'UPenn',
        degree: 'MS',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'NLP'],
    email: 'olivia.wang@example.com',
    matchScore: 84
  },
  {
    id: '14',
    name: 'Ryan Martinez',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    currentRole: 'ML Engineer',
    currentCompany: 'Perplexity AI',
    companyLogo: 'https://img.logo.dev/perplexity.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/gatech.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building AI-powered search systems.',
    experience: [
      {
        company: 'Perplexity AI',
        companyLogo: 'https://img.logo.dev/perplexity.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Developing AI search technology.'
      }
    ],
    education: [
      {
        school: 'Georgia Tech',
        degree: 'MS',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'Search'],
    email: 'ryan.martinez@example.com',
    matchScore: 83
  },
  {
    id: '15',
    name: 'Isabella Brown',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    currentRole: 'Research Engineer',
    currentCompany: 'Mistral AI',
    companyLogo: 'https://img.logo.dev/mistral.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/ethz.ch?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'Paris, France',
    bio: 'Developing efficient language models.',
    experience: [
      {
        company: 'Mistral AI',
        companyLogo: 'https://img.logo.dev/mistral.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Research Engineer',
        duration: '2023 - Present',
        location: 'Paris, France',
        description: 'Working on efficient LLMs.'
      }
    ],
    education: [
      {
        school: 'ETH Zürich',
        degree: 'MS',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'NLP'],
    email: 'isabella.brown@example.com',
    matchScore: 82
  },
  {
    id: '16',
    name: 'Lucas Thompson',
    avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
    currentRole: 'Robotics Engineer',
    currentCompany: 'Figure AI',
    companyLogo: 'https://img.logo.dev/figure.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/stanford.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Building humanoid robots.',
    experience: [
      {
        company: 'Figure AI',
        companyLogo: 'https://img.logo.dev/figure.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Robotics Engineer',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Developing humanoid robots.'
      }
    ],
    education: [
      {
        school: 'Stanford University',
        degree: 'MS',
        field: 'Robotics',
        year: '2023'
      }
    ],
    skills: ['Python', 'ROS', 'Control'],
    email: 'lucas.thompson@example.com',
    matchScore: 81
  },
  {
    id: '17',
    name: 'Sophia Rodriguez',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    currentRole: 'AI Researcher',
    currentCompany: 'Midjourney',
    companyLogo: 'https://img.logo.dev/midjourney.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/mit.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'San Francisco, CA',
    bio: 'Working on generative AI for images.',
    experience: [
      {
        company: 'Midjourney',
        companyLogo: 'https://img.logo.dev/midjourney.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'AI Researcher',
        duration: '2023 - Present',
        location: 'San Francisco, CA',
        description: 'Developing image generation models.'
      }
    ],
    education: [
      {
        school: 'MIT',
        degree: 'PhD',
        field: 'Computer Vision',
        year: '2023'
      }
    ],
    skills: ['Python', 'CV', 'GANs'],
    email: 'sophia.rodriguez@example.com',
    matchScore: 80
  },
  {
    id: '18',
    name: 'William Clark',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    currentRole: 'Research Scientist',
    currentCompany: 'Stability AI',
    companyLogo: 'https://img.logo.dev/stability.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/berkeley.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'London, UK',
    bio: 'Developing stable diffusion models.',
    experience: [
      {
        company: 'Stability AI',
        companyLogo: 'https://img.logo.dev/stability.ai?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'Research Scientist',
        duration: '2023 - Present',
        location: 'London, UK',
        description: 'Working on diffusion models.'
      }
    ],
    education: [
      {
        school: 'UC Berkeley',
        degree: 'PhD',
        field: 'Computer Vision',
        year: '2023'
      }
    ],
    skills: ['Python', 'CV', 'Diffusion'],
    email: 'william.clark@example.com',
    matchScore: 79
  },
  {
    id: '19',
    name: 'Ava Patel',
    avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9',
    currentRole: 'ML Engineer',
    currentCompany: 'Hugging Face',
    companyLogo: 'https://img.logo.dev/huggingface.co?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/cambridge.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'New York, NY',
    bio: 'Building open-source ML tools.',
    experience: [
      {
        company: 'Hugging Face',
        companyLogo: 'https://img.logo.dev/huggingface.co?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2023 - Present',
        location: 'New York, NY',
        description: 'Developing ML libraries and tools.'
      }
    ],
    education: [
      {
        school: 'Cambridge University',
        degree: 'MPhil',
        field: 'Machine Learning',
        year: '2023'
      }
    ],
    skills: ['Python', 'ML', 'NLP'],
    email: 'ava.patel@example.com',
    matchScore: 78
  },
  {
    id: '20',
    name: 'Ethan Kim',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    currentRole: 'ML Engineer',
    currentCompany: 'Runway',
    companyLogo: 'https://img.logo.dev/runwayml.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    schoolLogo: 'https://img.logo.dev/nyu.edu?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
    location: 'New York, NY',
    bio: 'Working on generative AI for video.',
    experience: [
      {
        company: 'Runway',
        companyLogo: 'https://img.logo.dev/runwayml.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ',
        role: 'ML Engineer',
        duration: '2023 - Present',
        location: 'New York, NY',
        description: 'Developing video generation models.'
      }
    ],
    education: [
      {
        school: 'NYU',
        degree: 'MS',
        field: 'Computer Science',
        year: '2023'
      }
    ],
    skills: ['Python', 'CV', 'GANs'],
    email: 'ethan.kim@example.com',
    matchScore: 77
  }
];