import requests

def generate_post(business, tone, platform) -> str:
    prompt = f"Write a social media post about {business} in a {tone} tone for {platform}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral:latest", "prompt": prompt, "stream": False},
    )
    print(response)
    if response.status_code != 200:
        return "Error generating post"
    data = response.json()
    return data.get("response", "No response from model")



generate_post("AI in healthcare", "informative", "LinkedIn")