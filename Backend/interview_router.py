from fastapi import APIRouter
from schemas import AnswerInput
from ai_interviews import generate_question, evaluate_answer

router = APIRouter()

@router.get("/question")
async def get_question(topic: str = "Python"):
    question = await generate_question(topic)
    return {"question": question}

@router.post("/evaluate")
async def evaluate(data: AnswerInput):
    result = await evaluate_answer(data.question, data.answer)
    return {"evaluation": result}
