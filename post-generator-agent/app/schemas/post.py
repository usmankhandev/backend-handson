from pydantic import BaseModel

class PostRequest(BaseModel):
    tone: str
    platform: str
    business: str
    
class PostResponse(BaseModel):
    post: str