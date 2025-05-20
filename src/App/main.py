from fastapi import FastAPI
from src.Controller.interview_controller import router

app = FastAPI(title="AI Interview (Groq + LLaMA3)")

app.include_router(router, prefix="/interview", tags=["Interview"])
