from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    схема для создания
    пользователя
    таблицы Users
    """
    id_google_client:str
    email: str
    password: Optional[str]=''
    access: Optional[bool] = True
    spent_day_limit: int
