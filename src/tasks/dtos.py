from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    desctiption:str
    completed:bool = False