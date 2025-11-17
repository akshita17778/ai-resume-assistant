# AI Resume Assistant

A minimal Flask web app that helps generate a resume summary, experience bullets, and skills using an AI model (OpenAI or Anthropic/Claude).

Features
- Small web UI to input name, experience, skills, and target job
- Backend endpoint `/api/generate` calls an AI provider and returns structured JSON
- Provider selection via `PROVIDER` env var (`openai` or `anthropic`)

Security note
- Keep API keys secret. Add them to your environment or a `.env` file (do NOT commit `.env` to git).

Quick start (local)

1. Copy `.env.example` to `.env` and fill your API keys.

2. Create and activate a virtual environment (Windows PowerShell example):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the app:

```powershell
$env:FLASK_APP = 'app.py'; $env:FLASK_ENV = 'development'; flask run --host=0.0.0.0 --port=5000
```

4. Open `http://localhost:5000` in your browser.

Using Claude Haiku (Anthropic)
- This repo includes example code to call Anthropic's completion endpoint. You must have an Anthropic API key and model access (e.g. `claude-haiku-4.5`).
- Set `PROVIDER=anthropic` and `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` in your `.env`.

Notes about "Enable Claude Haiku 4.5 for all clients"
- I cannot enable or change model access on Anthropic's platform from here. Model access is controlled by Anthropic and your account/organization settings. If you need to enable a model for all clients in your organization, contact Anthropic support or use your Anthropic admin console.

Extending and deployment
- Deploy to platforms like Render, Fly, or Railway. For production, secure API keys and consider serverless functions or an API gateway.

License
- MIT (use as you like)
