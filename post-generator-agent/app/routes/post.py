from fastapi import APIRouter, Depends
from app.schemas.response import APIResponse
from app.services.ai_service import generate_post
from app.schemas.post import PostRequest, PostResponse
from app.models.post import Post
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from db.dependencies import get_db

router = APIRouter()



@router.post("/generate", response_model=APIResponse[PostResponse])
async def generate_social_media_post(data: PostRequest, db: Session = Depends(get_db)):
    content = generate_post(data.business, data.tone, data.platform)
    
    post = Post(
        business=data.business,
        platform=data.platform,
        tone=data.tone,
        content=content
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    
    return PostResponse(post = content)
