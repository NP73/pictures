import queue
from repositories.users import Users

from fastapi import (APIRouter,
                     File,
                     UploadFile,
                     BackgroundTasks
                     )


from schemas import pictures
from service import users
from service.pictures import save_origin_image


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
async def create(picture: pictures.PictureCreate):
    picture_dict = await reverse_dict_for_str_picture(picture)
    return await Pictures.objects.create(**picture_dict.dict())

  


@pictureapp.get('/')
async def get_all():
    return await Pictures.objects.all()


@pictureapp.get('/{id}')
async def get_one(id: int):
    picture = await Pictures.objects.get_or_none(id=id)
    return await reverse_str_for_dict_picture(picture)


@pictureapp.post("/uploadimages/{user_google_id}")
async def create_upload_file(user_google_id: str,image: UploadFile = File(...)):
    
    user_asses = await Users.objects.get(id_google_client=user_google_id)
    if user_asses.access:
        user, count_limit = await users.get_count_images_user_id(user_google_id)
        if user:
            await save_origin_image(user_google_id,image)
            return {'message': True, "limit": f'{user_asses.spent_day_limit}/5','asses':user_asses.access}
        else:
            return {'message': False, "limit": f'{count_limit}/5','asses':user_asses.access}

    else:
         return {'message': False, "limit": f'{user_asses.spent_day_limit}/5','asses':user_asses.access}
   
    






    
