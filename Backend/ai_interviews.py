import os
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path="key.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def call_groq(messages):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GROQ_API_URL,
            headers=headers,
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7
            }
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def generate_question(topic: str) -> str:
    messages = [
        {"role": "user", "content": f"Hãy đặt một câu hỏi phỏng vấn kỹ thuật về chủ đề {topic}."}
    ]
    return await call_groq(messages)

async def evaluate_answer(question: str, answer: str) -> str:
    messages = [
        {"role": "user", "content": f"""Bạn là nhà tuyển dụng.  
Câu hỏi: "{question}"  
Câu trả lời của ứng viên: "{answer}"  
Hãy đánh giá ngắn gọn câu trả lời và cho điểm từ 1 đến 10."""}
    ]
    return await call_groq(messages)
