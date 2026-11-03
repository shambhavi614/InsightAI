
import time
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api"
MODEL_NAME = "llama3.2:1b"



def check_ollama():
    try:
        response = requests.get(
            f"{OLLAMA_URL}/tags",
            timeout=10
        )
        response.raise_for_status()

        models = [
            model.get("name", "")
            for model in response.json().get("models", [])
        ]

        return MODEL_NAME in models

    except requests.RequestException:
        return False


def ask_ai(question):
    start_time = time.perf_counter()

    try:
        response = requests.post(
            f"{OLLAMA_URL}/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are InsightAI, a concise "
                            "data analytics assistant. "
                            "Answer clearly in under 100 words. "
                            "Never invent dataset results."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "stream": False,
                
"options": {
    "temperature": 0.1,
    "num_predict": 160,
    "num_ctx": 1024
},

                "keep_alive": "10m"
            },
            timeout=(10, 180)
        )

        response.raise_for_status()
        result = response.json()

        answer = result["message"]["content"]
        elapsed = time.perf_counter() - start_time

        return (
            f"{answer}\n\n"
            f"---\n"
            f"⏱ Response time: {elapsed:.1f}s"
        )

    except requests.exceptions.Timeout:
        return (
            "The AI response timed out. "
            "Try a shorter question or check "
            "Ollama performance."
        )

    except requests.RequestException as e:
        return f"Ollama connection error: {e}"

    except (KeyError, ValueError) as e:
        return f"Unexpected AI response: {e}"
