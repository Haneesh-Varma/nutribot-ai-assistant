# NutriBot

NutriBot is a small nutrition chatbot built with Python and Flask. It sends a user's question to the Groq API and returns a general nutrition-focused answer.

## Features

- Ask general questions about food and nutrition
- Keep a short conversation history between requests
- Use an API key stored outside the source code
- Return clear errors when the API key is missing or the service is unavailable

## Requirements

- Python 3.10 or newer
- A Groq account and API key

## Setup

Create and activate a virtual environment, then install the packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own API key. Do not commit the `.env` file.

```bash
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your key. The app reads these values when it starts.

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`.

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/` | Check that the API is running |
| POST | `/chat` | Send a nutrition question to NutriBot |

### Example request

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What are some affordable sources of protein?"}'
```

To continue a conversation, send earlier messages in the `history` list:

```json
{
  "message": "Can you give me a few vegetarian options?",
  "history": [
    {"role": "user", "content": "What are some affordable sources of protein?"},
    {"role": "assistant", "content": "Examples include lentils, beans, milk and eggs."}
  ]
}
```

## Model and API limits

The model name is configurable through `GROQ_MODEL`. The default is `openai/gpt-oss-20b`; model access and free-tier limits can change, so check the current Groq console if a request fails. Free access is rate-limited and is not unlimited.

## Safety note

NutriBot is for general nutrition education. It may make mistakes and cannot calculate exact nutritional needs or replace advice from a doctor or registered dietitian. Food and calorie estimates can vary by ingredients, serving size and preparation.

## Run the tests

```bash
python -m unittest discover -s tests -v
```
