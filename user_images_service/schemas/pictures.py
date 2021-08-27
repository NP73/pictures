from pydantic import BaseModel
import pydantic

from typing import Optional


class PictureCreate(BaseModel):
    user_id_google: str
    img_link: str
    settings: dict
    status: bool
    result_imgs_link: dict
    result_dict: dict


class PictureInfo(PictureCreate):
    id: int
    timestamp: str
