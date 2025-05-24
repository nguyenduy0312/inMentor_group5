from pydantic import BaseModel

class StartInput(BaseModel):
    user_id: str

class AnswerInput(BaseModel):
    ma_phien: int
    topic: str
    question: str
    answer: str

class FinishInput(BaseModel):
    ma_phien: int
    report: str