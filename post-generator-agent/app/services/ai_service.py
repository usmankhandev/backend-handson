import requests
from app.templates.template_router import build_prompt

def generate_post(business, tone, platform) -> str:
    prompt = build_prompt(platform, business, tone)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral:latest", "prompt": prompt, "stream": False},
    )
    print(response)
    if response.status_code != 200:
        return "Error generating post"
    data = response.json()
    return data.get("response", "No response from model")
