from pydantic import BaseModel

class TextToAnswer(BaseModel): 
    question: str
    
class newQuestion(BaseModel): 
    question: str
    answer:str
    
class editQuestion(BaseModel):
    id:int
    question: str
    answer: str
    
class deleteQuestion(BaseModel):
    id:int