exports.handler = async function(event) {
  // Hanya izinkan metode POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    // Ambil payload (pesan chat) dari frontend
    const body = JSON.parse(event.body);
    
    // Ambil API Key RAHASIA dari environment variable di Netlify
    const GROQ_API_KEY = process.env.GROQ_API_KEY;

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body) // Teruskan payload ke Groq
    });

    if (!response.ok) {
        throw new Error(`Groq API request failed with status ${response.status}`);
    }

    // Kembalikan respons dari Groq langsung ke frontend
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: await response.text(),
    };

  } catch (error) {
    console.error('Error in serverless function:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    };
  }
};