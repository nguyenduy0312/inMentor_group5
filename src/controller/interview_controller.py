from fastapi import APIRouter 
from src.model.schemas import AnswerInput
from src.services.ai_service import generate_question, evaluate_answer

router = APIRouter()

@router.get("/question")
async def get_question(topic: str = "Python"):
    question = await generate_question(topic)
    return {"question": question}

@router.post("/evaluate")
async def evaluate(data: AnswerInput):
    result = await evaluate_answer(data.question, data.answer)
    return {"evaluation": result}
