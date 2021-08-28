from pydantic import BaseModel
import pydantic

from typing import Optional


class PictureCreate(BaseModel):
    user_id_google: str
    img_link: str
    settings: dict
    status: bool
    result_dict: dict


class PictureInfo(PictureCreate):
    id: int
    timestamp: str


class PictureUpdate(BaseModel):
    origin_img_id :int
    result_dict: str
    status: bool


class LinkImage(BaseModel):
    img_link:str

        #    "user_id_google":localStorage.getItem('google_id'),
        # "img_link": result.img_link,
        # "origin_img_id":result.origin_img_id,
        # "settings": String(result.result_dict),
        # "status": true,
        # "result_imgs_link": "{}",
        # "result_dict": String(result.result_dict),