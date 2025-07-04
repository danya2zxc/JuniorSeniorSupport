from fastapi import FastAPI

from src.ai.router import router as ai_router
from src.auth.router import router as auth_router
from src.issues.router import router as issues_router
from src.users.router import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(issues_router, prefix="/api", tags=["issues"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(ai_router, prefix="/api", tags=["Chatbot"])
