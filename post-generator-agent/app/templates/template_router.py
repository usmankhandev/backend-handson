from app.templates.prompt_template import TEMPLATES

SUPPORTED_PLATFORMS = set(TEMPLATES.keys());

def get_template(platform: str) -> str:
    """
    Takes a platform name, returns the matching prompt template string.
    Raises a clear error if platform is unsupported.

    """

    platform = platform.lower()
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform '{platform}'. Supported platforms: {', '.join(SUPPORTED_PLATFORMS)}")
    
    return TEMPLATES[platform]


def build_prompt(platform: str, topic: str, tone: str) -> str:
    """
    Builds the final prompt string by filling in the template with the provided topic and tone.
    """

    template = get_template(platform)
    prompt = template.format(topic=topic, tone=tone)
    return prompt
    
