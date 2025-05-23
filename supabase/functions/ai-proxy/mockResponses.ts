import { Category } from './types.ts';

export const mockResponses: Record<Category, string[]> = {
  jobs: [
    "Based on current market trends, I recommend focusing on full-stack development roles. Key skills to highlight: React, Node.js, and cloud services. Consider applying to tech startups - they're actively hiring!",
    "The tech job market is showing strong demand for AI/ML engineers and data scientists. Companies like OpenAI and Anthropic are expanding their teams significantly.",
    "Remote work opportunities have increased by 30% this year. Many companies are offering competitive packages including equity and flexible work arrangements."
  ],
  research: [
    "Recent studies in computer science are focusing on AI safety and ethical implementations. Key areas include: explainable AI, bias detection, and sustainable computing practices.",
    "Quantum computing research is gaining momentum, with several universities leading breakthrough studies in quantum algorithms and error correction.",
    "The latest research papers emphasize advancements in machine learning architectures. Transformer models and few-shot learning are particularly active areas."
  ],
  clubs: [
    "Consider joining coding clubs that focus on practical project building. Hackathon groups are excellent for networking and skill development.",
    "Tech meetups and open source communities are great places to start. Many offer mentorship programs and collaborative learning opportunities.",
    "Local developer communities and online coding forums provide valuable connections. Look for groups that align with your specific interests."
  ],
  courses: [
    "Popular online courses include Advanced React Patterns, System Design, and Cloud Architecture. These align well with current industry demands.",
    "I recommend starting with fundamental CS courses, then specializing in areas like distributed systems or AI/ML. Many universities offer open courseware.",
    "Focus on practical courses that teach modern tech stacks. Full-stack development bootcamps and specialized certifications are worth considering."
  ]
};