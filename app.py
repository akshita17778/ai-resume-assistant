import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

PROVIDER = os.getenv('PROVIDER', 'openai').lower()

# OpenAI defaults
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# Anthropic defaults (for Claude Haiku or other Claude models)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-haiku-4.5')


@app.route('/')
def index():
    return render_template('index.html')


def build_prompt(data):
    # Basic instruction to the model to produce a resume summary and bullet points
    prompt = f"""
You are a professional resume writer. Given the following user information, produce:
1) A one-paragraph professional summary suitable for a resume.
2) A set of concise bullet points (3-6) describing the user's most recent role or an exemplary role, focusing on impact and metrics where possible.
3) A short skills list (comma separated).

Return only JSON with keys: `summary`, `experience_bullets` (array), `skills` (array).

User info:
Name: {data.get('name','')}
Current title / target title: {data.get('title','')}
Experience (free text): {data.get('experience','')}
Skills: {data.get('skills','')}
Target job: {data.get('target_job','')}
Tone: {data.get('tone','professional')}

Use a {data.get('tone','professional')} tone and prioritize clarity and ATS-friendly wording.
"""
    return prompt


def call_openai(prompt):
    import openai
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = OPENAI_API_KEY
    model = OPENAI_MODEL
    # Use ChatCompletion for structured prompt
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs JSON as requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600,
        )
        text = resp['choices'][0]['message']['content']
        return text
    except Exception as e:
        raise


def call_anthropic(prompt):
    # Call Anthropic completion endpoint. This is a best-effort example.
    if not ANTHROPIC_API_KEY:
        raise RuntimeError('ANTHROPIC_API_KEY not set')
    url = 'https://api.anthropic.com/v1/complete'
    headers = {
        'x-api-key': ANTHROPIC_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'model': ANTHROPIC_MODEL,
        'prompt': prompt,
        'max_tokens': 600,
        'temperature': 0.2,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    # Anthropic responses typically put text in `completion`
    text = j.get('completion') or j.get('output') or json.dumps(j)
    return text


@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    prompt = build_prompt(data)
    try:
        if PROVIDER == 'anthropic' or PROVIDER == 'claude':
            text = call_anthropic(prompt)
        else:
            text = call_openai(prompt)

        # Attempt to parse JSON from the model output; fall back to raw text
        try:
            parsed = json.loads(text)
        except Exception:
            # If model returned text, put it in a key
            parsed = {"raw_text": text}

        return jsonify({"ok": True, "result": parsed})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
