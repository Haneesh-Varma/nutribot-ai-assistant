import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
SYSTEM_MESSAGE = """You are NutriBot, a friendly assistant for general nutrition education.
Give practical, balanced information in simple language. Explain when food values
are estimates and can vary by portion size and preparation. Do not diagnose illnesses,
prescribe diets for medical conditions, recommend extreme restriction, or replace a
registered dietitian or doctor. If a question involves a medical condition, pregnancy,
an eating disorder, or urgent symptoms, encourage the user to speak with a qualified
health professional. Do not pretend to know a person's exact nutritional needs."""


def get_bot_reply(message, history):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your environment.")

    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    for item in history[-8:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str):
            messages.append({"role": role, "content": content[:2000]})
    messages.append({"role": "user", "content": message})

    response = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.6, "max_tokens": 700},
        timeout=45
    )
    if response.status_code == 429:
        raise RuntimeError("The API rate limit was reached. Please wait and try again.")
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


@app.get("/")
def home():
    return jsonify({"message": "NutriBot API is running", "model": GROQ_MODEL})


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message")
    history = data.get("history", [])
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please provide a message"}), 400
    if not isinstance(history, list):
        return jsonify({"error": "history must be a list"}), 400

    try:
        reply = get_bot_reply(message.strip()[:2000], history)
        return jsonify({"reply": reply, "model": GROQ_MODEL})
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503
    except requests.Timeout:
        return jsonify({"error": "The AI service took too long to respond. Try again."}), 504
    except requests.RequestException:
        return jsonify({"error": "Could not reach the AI service. Check your connection and API settings."}), 502
    except (KeyError, IndexError, TypeError, ValueError):
        return jsonify({"error": "The AI service returned an unexpected response"}), 502


if __name__ == "__main__":
    app.run(debug=True)
