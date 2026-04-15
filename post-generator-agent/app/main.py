from fastapi import FastAPI
from app.db.session import engine
from app.routes import post
from app.db.base import Base
from app.models.post import Post



app = FastAPI()
app.include_router(post.router)

try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")