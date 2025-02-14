// node --version # Should be >= 18
// npm install @google/generative-ai express

const express = require('express');
const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require('@google/generative-ai');
const dotenv = require('dotenv')
dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
const MODEL_NAME = "gemini-pro";
const API_KEY = process.env.API_KEY;

async function runChatWithRetry(userInput, retries = 3, delay = 1000) { 
  try {
    const genAI = new GoogleGenerativeAI(API_KEY);
    const model = genAI.getGenerativeModel({ model: MODEL_NAME });

    const generationConfig = {
      temperature: 0.9,
      topK: 1,
      topP: 1,
      maxOutputTokens: 1000,
    };

    const safetySettings = [
      {
        category: HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      },
    ];

    const chat = model.startChat({
      generationConfig,
      safetySettings,
      history: [
        {
          role: "user",
          parts: [{ text: "You are Hua, a friendly assistant for AI Chatbot. Chatbot is a website that assists people to learn what interested." }],
        },
        {
          role: "model",
          parts: [{ text: "Hello! Welcome to Chatbot! My name is Hua. What's your name?" }],
        },
        {
          role: "user",
          parts: [{ text: "Hi" }],
        },
        {
          role: "model",
          parts: [{ text: "Hi there! Thanks for reaching out us! What can I help you today?" }],
        },
      ],
    });

    const result = await chat.sendMessage(userInput); // Now using userInput
    const response = result.response;
    return response.text();
  } catch (error) {
      if (error.message.includes("503 Service Unavailable") || error.message.includes("429 Too Many Requests")) {
        if (retries > 0) {
          console.log(`Gemini API overloaded/rate limited. Retrying in ${delay}ms... (Retries left: ${retries - 1})`);
          await new Promise(resolve => setTimeout(resolve, delay));
          return runChatWithRetry(userInput, retries - 1, delay * 2); // Exponential backoff
        } else {
          console.error("Gemini API Error (after retries):", error);
          throw error; // Re-throw to be handled by the route handler
        }
      } else {
        console.error("Gemini API Error:", error);
        throw error; // Re-throw other errors
      }
    }  
  }

app.use(express.static('public')); // Express middleware static files saved in 'public' directory

app.get('/', (req, res) => {
  res.sendFile(__dirname + 'index.html');
});
app.get('/loader.gif', (req, res) => {
  res.sendFile(__dirname + '/loader.gif');
});
app.post('/chat', async (req, res) => {
  try {
    const userInput = req.body?.userInput;
    console.log('incoming /chat req', userInput)
    if (!userInput) {
      return res.status(400).json({ error: 'Invalid request body' });
    }

    const response = await runChatWithRetry(userInput);
    res.json({ response });
  } catch (error) {
    console.error('Error in chat endpoint:', error);
    res.status(503).json({ error: 'Gemini API is currently unavailable. Please try again later.' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
