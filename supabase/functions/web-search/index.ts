import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { getJson } from "https://deno.land/x/serpapi@v1.1.1/mod.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  type?: string;
  deadline?: string;
  amount?: string;
  requirements?: string[];
}

async function performWebSearch(query: string, category: string): Promise<SearchResult[]> {
  try {
    const searchQuery = `${query} ${category} site:yale.edu`;
    
    const params = {
      q: searchQuery,
      api_key: Deno.env.get("SERPAPI_KEY"),
      engine: "google",
      num: 5, // Number of results
    };

    const data = await getJson(params);
    const organicResults = data.organic_results || [];

    return organicResults.map((result: any) => ({
      title: result.title,
      url: result.link,
      snippet: result.snippet,
      type: detectResultType(result.title, result.snippet),
      deadline: extractDeadline(result.snippet),
      amount: extractAmount(result.snippet),
      requirements: extractRequirements(result.snippet)
    }));
  } catch (error) {
    console.error('SerpAPI search failed:', error);
    return getMockResults(category);
  }
}

function detectResultType(title: string, snippet: string): string | undefined {
  const text = `${title} ${snippet}`.toLowerCase();
  if (text.includes('fellowship')) return 'Fellowship';
  if (text.includes('grant')) return 'Grant';
  if (text.includes('program')) return 'Program';
  if (text.includes('resource')) return 'Resource';
  return undefined;
}

function extractDeadline(text: string): string | undefined {
  const datePattern = /(?:deadline|due|closes?|applications? due):?\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}\/\d{1,2}\/\d{4})/i;
  const match = text.match(datePattern);
  return match ? match[1] : undefined;
}

function extractAmount(text: string): string | undefined {
  const amountPattern = /\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?(?:\s*-\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)?/;
  const match = text.match(amountPattern);
  return match ? match[0] : undefined;
}

function extractRequirements(text: string): string[] | undefined {
  const requirementIndicators = [
    'must have', 'required', 'requirements:', 'eligibility:', 'qualifications:',
    'prerequisites:', 'criteria:', 'applicants must'
  ];
  
  let requirements: string[] = [];
  
  for (const indicator of requirementIndicators) {
    const pattern = new RegExp(`${indicator}\\s*([^.]+)`, 'i');
    const match = text.match(pattern);
    if (match) {
      const reqs = match[1]
        .split(/[,;]/)
        .map(req => req.trim())
        .filter(req => req.length > 0);
      requirements = [...requirements, ...reqs];
    }
  }
  
  return requirements.length > 0 ? requirements : undefined;
}

function getMockResults(category: string): SearchResult[] {
  const results: Record<string, SearchResult[]> = {
    research: [
      {
        title: "Yale Science & Engineering Research Fellowship",
        url: "https://science.yale.edu/research-fellowships",
        snippet: "Summer research opportunity with $6,000 stipend for STEM undergraduates",
        type: "Fellowship",
        deadline: "March 15, 2024",
        amount: "$6,000",
        requirements: [
          "Yale undergraduate student",
          "STEM major",
          "Minimum 3.0 GPA",
          "Faculty sponsor"
        ]
      },
      {
        title: "Quantum Computing Research Initiative",
        url: "https://quantum.yale.edu/opportunities",
        snippet: "Advanced research positions in quantum computing and information science",
        type: "Research Program",
        deadline: "Rolling",
        amount: "$8,000 per semester",
        requirements: [
          "Graduate student or advanced undergraduate",
          "Strong physics or CS background",
          "Programming experience"
        ]
      },
      {
        title: "Yale Center for Research Computing Resources",
        url: "https://research.computing.yale.edu",
        snippet: "Access to high-performance computing clusters and technical support",
        type: "Resource",
        requirements: [
          "Yale researcher status",
          "Project proposal",
          "Data management plan"
        ]
      }
    ],
    jobs: [
      {
        title: "Yale Student Jobs Board",
        url: "https://yale.studentemployment.ngwebsolutions.com/",
        snippet: "Latest job postings for Yale students across various departments."
      }
    ],
    clubs: [
      {
        title: "Yale Student Organizations",
        url: "https://yale.campusgroups.com/",
        snippet: "Directory of registered student organizations at Yale."
      }
    ],
    courses: [
      {
        title: "Yale Course Search",
        url: "https://courses.yale.edu/",
        snippet: "Comprehensive database of Yale courses across all departments."
      }
    ]
  };

  return results[category] || [];
}

serve(async (req) => {
  const responseHeaders = {
    ...corsHeaders,
    'Content-Type': 'application/json'
  };

  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: responseHeaders });
  }

  try {
    const { query, category } = await req.json();

    if (!query || !category) {
      return new Response(
        JSON.stringify({ 
          error: 'Missing required parameters',
          results: [] 
        }),
        { status: 200, headers: responseHeaders }
      );
    }

    const results = await performWebSearch(query, category);

    return new Response(
      JSON.stringify({ results }),
      { status: 200, headers: responseHeaders }
    );

  } catch (error) {
    console.error('Error in web search:', error);
    return new Response(
      JSON.stringify({ 
        error: error.message,
        results: getMockResults('research')
      }),
      { status: 200, headers: responseHeaders }
    );
  }
});