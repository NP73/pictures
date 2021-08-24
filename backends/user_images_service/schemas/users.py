from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str 
    password: str 
    access:bool 
    spent_day_limit: int 