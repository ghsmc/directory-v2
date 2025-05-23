const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

async function callAIProxy(model: string, query: string, category: string, onUpdate: (text: string) => void) {
  try {
    // Validate environment variables
    if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
      throw new Error('Missing required environment variables: SUPABASE_URL or SUPABASE_ANON_KEY');
    }

    const functionUrl = `${SUPABASE_URL}/functions/v1/ai-proxy`;
    console.log(`Calling ${model} API with query:`, query);
    console.log('Function URL:', functionUrl);
    
    const response = await fetch(functionUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      },
      body: JSON.stringify({ model, query, category }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }

    // Stream the response character by character
    let currentText = '';
    for (const char of data.response) {
      currentText += char;
      onUpdate(currentText);
      await new Promise(resolve => setTimeout(resolve, 10));
    }

    return data.response;
  } catch (error) {
    console.error(`${model} API Error:`, error);
    // Log additional debugging information
    console.error('Environment variables status:', {
      hasSupabaseUrl: !!SUPABASE_URL,
      hasSupabaseKey: !!SUPABASE_ANON_KEY,
    });
    
    const errorMessage = "An error occurred while processing your request. Please try again later.";
    onUpdate(errorMessage);
    return errorMessage;
  }
}

export async function getGPTResponse(query: string, category: string, onUpdate: (text: string) => void) {
  return callAIProxy('gpt4', query, category, onUpdate);
}

export async function getClaudeResponse(query: string, category: string, onUpdate: (text: string) => void) {
  return callAIProxy('claude', query, category, onUpdate);
}

export async function getPerplexityResponse(query: string, category: string, onUpdate: (text: string) => void) {
  return callAIProxy('perplexity', query, category, onUpdate);
}