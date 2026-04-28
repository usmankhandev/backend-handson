TEMPLATES = {
    "X_SOCIAL_MEDIA_POST": """
    You are a social media expert writing for X (Twitter).
    Write a post about: {topic}
    Tone: {tone}
    Rules:
    - Max 280 characters
    - Use 1–2 hashtags max
    - No fluff, punchy and direct
    - Include a CTA if relevant

    Return only the post text.
    """",
     "linkedin": """
    You are a professional content writer for LinkedIn.
    Write a post about: {topic}
    Tone: {tone}
    Rules:
    - 150–300 words
    - Start with a strong hook (first line must grab attention)
    - Use short paragraphs (2–3 lines max)
    - End with a question or CTA to drive comments
    - 3–5 relevant hashtags at the end

    Return only the post text.
    """,

    "instagram": """
    You are a creative social media writer for Instagram.
    Write a caption about: {topic}
    Tone: {tone}
    Rules:
    - 100–150 words
    - Conversational and warm
    - Use line breaks for readability
    - End with 5–10 hashtags on a new line
    - Include an emoji or two naturally

    Return only the post text.
    """

}