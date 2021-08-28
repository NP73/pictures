import datetime
import ast

from pydantic import validator
import ormar


from config.database import metadata, database
import json


class Pictures(ormar.Model):

    """
        id -  id изображения
        user_id - id пользователя , который добавил изображение  
        img_link - ссылка на исходную картинку, 
        settings - (словарь настроек. в одно поле весь словарь пишем как текст), 
        status -  (false  если обработка не закончена,  если закончена true), 
        result_imgs_link (ссылка на папку с результирующими картинками)
        result_dict (некоторый словарь который получается в результате обсчета)
        timestamp - дата и время добавления изображения 
    """

    class Meta:
        tablename = "pictures_table"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user_id_google: str = ormar.String(max_length=1000)
    img_link: str = ormar.String(max_length=1000)
    settings: str = ormar.String(max_length=1000)
    status: bool = ormar.Boolean(default=False)
    result_imgs_link: str = ormar.String(max_length=10000)
    result_dict: str = ormar.String(max_length=1000)
    timestamp: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now)

    class Config:
        orm_mode = True
