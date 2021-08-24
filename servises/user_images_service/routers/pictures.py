from fastapi import APIRouter, File, UploadFile
 

from schemas import pictures


from repositories.pictures import Pictures
from service.pictures import (
                            reverse_dict_for_str_picture,
                            reverse_str_for_dict_picture
                            )

pictureapp = APIRouter(
    prefix="/api/v1/pictures",
    responses={404: {"description": "Not found"}}
)


@pictureapp.post('/')
async def create(picture:pictures.PictureCreate):
    picture_dict = await reverse_dict_for_str_picture(picture)
    return await Pictures.objects.create(**picture_dict.dict())

@pictureapp.get('/')
async def get_all():
    return await Pictures.objects.all()


@pictureapp.get('/{id}')
async def get_one(id:int):
    picture =  await Pictures.objects.get_or_none(id=id)
    return await reverse_str_for_dict_picture(picture)


@pictureapp.post("/uploadimages/")
async def create_upload_file(image: UploadFile = File(...)):
    return {"filename": image.filename}