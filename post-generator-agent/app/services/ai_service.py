from dotenv import load_dotenv as loadEnv
import os

loadEnv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(business, tone, platform) -> str:
    
    prompt = f"Write a social media post about {business} in a {tone} tone for {platform}"
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": prompt}
        ]
    )
    print(response)



generate_post("AI in healthcare", "informative", "LinkedIn")