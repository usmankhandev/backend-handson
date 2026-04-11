from fastapi import APIRouter
from app.services.ai_service import generate_post

router = APIRouter()

@router.post("/generate")
def generate_social_media_post(data: dict):
    business = data.get("business")
    platform = data.get("platform")
    tone = data.get("tone")
    
    result = generate_post(business, tone, platform)
    return {"post": result}
