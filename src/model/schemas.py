from pydantic import BaseModel

class AnswerInput(BaseModel):
    question: str
    answer: str
