from repositories.users import Users
import ast


from fastapi import (
                    APIRouter,
                    File,
                    UploadFile,
                    Depends
                    )
from fastapi.responses import JSONResponse

from schemas import pictures
from service import users
from service.pictures import save_origin_image
from service import profile_token

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


@pictureapp.get('/status-image-process/{id_image}')
async def status_image_upload(id_image:str, curent_user = Depends(profile_token.JWTBearer())):
    if type(curent_user) != str:
        return JSONResponse(
        status_code=400,
        content={
            "status": "badd",
            "detail": "Пользователь не авторизован",
        },
    )
    else:
        picture = await Pictures.objects.get_or_none(id=id_image)
        if picture.user_id_google != curent_user:
            return JSONResponse(
            status_code=400,
            content={
            "status": "badd",
            "detail": "Пользователь не относиться к данному изображению",
            }
            )
        else:
            try:
                return await reverse_str_for_dict_picture(picture)
            except:
                return {'message':'нет такого изображения'}
        




@pictureapp.post('/add_link_img/{id_img_origin}')
async def add_result_img_link_for_origin(id_img_origin: int,link_image:pictures.LinkImage):
    picture = await Pictures.objects.get_or_none(id=id_img_origin)
    result_linc = ast.literal_eval(picture.result_imgs_link)
    result_linc[str(len(result_linc)+1)] = link_image.img_link
    
    await picture.update(
        result_imgs_link = str(result_linc)
    )
    return {
        'result_imgs_link':link_image.img_link,
        'count_res_image':len(result_linc)
        }

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
   
    






    
