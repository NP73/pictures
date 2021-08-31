from pydantic import BaseModel
import pydantic

from typing import Optional


class PictureCreate(BaseModel):
    """
    схема для создания
    оригинального изображения
    таблицы Pictures
    """
    user_id_google: str
    img_link: str
    settings: dict
    status: bool
    result_dict: dict


class PictureInfo(PictureCreate):
    """
    схема для получения информации
    таблицы Pictures
    """
    id: int
    timestamp: str


class PictureUpdate(BaseModel):
    """
    схема для получения обновления 
    полей таблицы Pictures
    """
    origin_img_id :int
    result_dict: str
    status: bool


class LinkImage(BaseModel):
    """
    схема для получения ссылки в словарь
    оригинального изображения
    таблицы Pictures
    """
    img_link:str

