# AI Resume Assistant

A minimal Flask web app that helps generate a resume summary, experience bullets, and skills using an AI model (OpenAI or Anthropic/Claude).

Features
- Small web UI to input name, experience, skills, and target job
- Backend endpoint `/api/generate` calls an AI provider and returns structured JSON
- Provider selection via `PROVIDER` env var (`openai` or `anthropic`)


License
- MIT (use as you like)

