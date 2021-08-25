from pydantic import BaseModel
import pydantic


class PictureCreate(BaseModel):
    user_id: int
    img_link: str
    settings: str
    status: bool
    result_imgs_link: dict
    result_dict: dict


class PictureInfo(PictureCreate):
    id: int
    timestamp: str
