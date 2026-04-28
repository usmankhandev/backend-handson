from pydantic import BaseModel, field_validator

class PostRequest(BaseModel):
    tone: str = "professional"
    platform: str
    business: str
    
    @field_validator("platform")
    @classmethod
    def validate_platform(cls, v):
        """Validate the requested platform and normalize it to lowercase."""
        supported_platforms = {"x_social_media_post", "linkedin", "instagram"}
        if v.lower() not in supported_platforms:
            raise ValueError(f"Unsupported platform '{v}'. Supported platforms: {', '.join(supported_platforms)}")
        return v.lower()
    
class PostResponse(BaseModel):
    post: str