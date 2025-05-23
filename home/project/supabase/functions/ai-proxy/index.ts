import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function generateMockResponse(query: string, category: string, model: string) {
  const responses = {
    jobs: {
      gpt4: "Based on current market trends, I recommend focusing on full-stack development roles. Key skills to highlight: React, Node.js, and cloud services. Consider applying to tech startups - they're actively hiring!",
      claude: "For job seekers in tech, I suggest exploring positions in AI/ML engineering or DevOps. These fields show strong growth. Your portfolio and GitHub presence are crucial for standing out.",
      perplexity: "Looking at recent data, software engineering roles remain in high demand. Focus on building practical projects and contributing to open source. Remote work opportunities have increased by 30% this year."
    },
    research: {
      gpt4: "Recent studies in computer science are focusing on AI safety and ethical implementations. Key areas include: explainable AI, bias detection, and sustainable computing practices.",
      claude: "Current research trends show increasing interest in quantum computing and its applications in cryptography. Several universities are leading breakthrough studies in this field.",
      perplexity: "The latest research papers emphasize advancements in machine learning architectures. Transformer models and few-shot learning are particularly active areas of study."
    },
    clubs: {
      gpt4: "Consider joining coding clubs that focus on practical project building. Hackathon groups are excellent for networking and skill development.",
      claude: "Tech meetups and open source communities are great places to start. Many offer mentorship programs and collaborative learning opportunities.",
      perplexity: "Local developer communities and online coding forums provide valuable connections. Look for groups that align with your specific interests in technology."
    },
    courses: {
      gpt4: "Popular online courses include Advanced React Patterns, System Design, and Cloud Architecture. These align well with current industry demands.",
      claude: "I recommend starting with fundamental CS courses, then specializing in areas like distributed systems or AI/ML. Many universities offer open courseware.",
      perplexity: "Focus on practical courses that teach modern tech stacks. Full-stack development bootcamps and specialized certifications are worth considering."
    }
  };

  // Default to 'research' if category not found
  const categoryResponses = responses[category as keyof typeof responses] || responses.research;
  return categoryResponses[model as keyof typeof categoryResponses] || "I'm sorry, I don't have specific information about that topic.";
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const { query, category, model } = await req.json();

    if (!query || !category || !model) {
      return new Response(
        JSON.stringify({ error: 'Missing required parameters' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // Reduced delay range: now between 200ms and 800ms
    await new Promise(resolve => setTimeout(resolve, Math.random() * 600 + 200));

    const response = generateMockResponse(query, category, model);

    return new Response(
      JSON.stringify({ response }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Error in AI proxy:', error);
    return new Response(
      JSON.stringify({ 
        error: error.message,
        type: error.name,
        details: error.stack
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );
  }
});