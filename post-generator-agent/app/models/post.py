from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    business = Column(String, index=True)
    platform = Column(String, index=True)
    tone = Column(String, index=True)
    content = Column(Text)
    
    
