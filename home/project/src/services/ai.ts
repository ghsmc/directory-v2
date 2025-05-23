const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

async function callAIProxy(model: string, query: string, category: string) {
  try {
    console.log(`Calling ${model} API with query:`, query);
    
    const response = await fetch(`${SUPABASE_URL}/functions/v1/ai-proxy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      },
      body: JSON.stringify({ model, query, category }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      console.error(`${model} API Error:`, data);
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }

    if (data.error) {
      console.error(`${model} Response Error:`, data.error);
      throw new Error(data.error);
    }

    return data.response;
  } catch (error) {
    console.error(`${model} API Error:`, error);
    return `Sorry, I encountered an error while processing your request: ${error.message}`;
  }
}

export async function getGPTResponse(query: string, category: string) {
  return callAIProxy('gpt4', query, category);
}

export async function getClaudeResponse(query: string, category: string) {
  return callAIProxy('claude', query, category);
}

export async function getPerplexityResponse(query: string, category: string) {
  return callAIProxy('perplexity', query, category);
}