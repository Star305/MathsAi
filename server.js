import express from "express";
import cors from "cors";
import fetch from "node-fetch";

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

// Put your OpenAI API key here (hidden from frontend)
const OPENAI_API_KEY = "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"; // <<< Replace with your key

// Endpoint to ask AI
app.post("/ask", async (req, res) => {
  const { question } = req.body;
  if (!question) return res.status(400).json({ error: "No question provided" });

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: "You are a helpful AI that solves math, science, and other school subjects in a fun way." },
          { role: "user", content: question }
        ],
        temperature: 0.7,
        max_tokens: 300
      }),
    });

    const data = await response.json();
    const answer = data.choices[0].message.content;
    res.json({ answer });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Something went wrong" });
  }
});

// Serve frontend (optional if you host frontend separately)
app.use(express.static("public")); // put index.html inside 'public' folder if using

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
