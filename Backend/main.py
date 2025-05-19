from fastapi import FastAPI
from interview_router import router

app = FastAPI(title="AI Interview (Groq + LLaMA3)")

app.include_router(router, prefix="/interview", tags=["Interview"])
