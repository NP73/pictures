from typing import Optional
from fastapi import APIRouter,  Depends,BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from repositories.users import Users
from repositories.pictures import Pictures
from schemas import users
from schemas.pictures import PictureUpdate
from service import profile_token, userauth


usersapp = APIRouter(
    prefix="/api/v1/users",
    responses={404: {"description": "Not found"}}
)




@usersapp.post('/')
async def create(user_data: users.UserCreate):
    access_token, access_token_expires = await userauth.user_service.virefity_profile(user_data)
    user = await Users.objects.get_or_none(id_google_client=user_data.id_google_client)
    
    cont = {"access_token": access_token,
            "access_token_expires": access_token_expires,
            "user_data": user,}
    json_compatible_item_data = jsonable_encoder(cont)
    return JSONResponse(
        status_code=200,
        content=json_compatible_item_data
    )

@usersapp.post('/token')
async def create_token(google_user_id: int):
    access_token, access_token_expires = await userauth.user_service.token_id(google_user_id)

    cont = {"access_token": access_token,
            "access_token_expires": access_token_expires,
            }
    json_compatible_item_data = jsonable_encoder(cont)
    return JSONResponse(
        status_code=200,
        content=json_compatible_item_data
    )


@usersapp.get('/')
async def get_all():
    return await Users.objects.all()



@usersapp.get('/{id}')
async def get_one(id: int):
    return await Users.objects.get_or_none(id=id)

@usersapp.post('/change_status/{id}')
async def update_status_user(id: str):
    user = await Users.objects.get_or_none(id_google_client=id)
    picture = await Pictures.objects.get_or_none(id=user.last_uploaded_image_id)
    return await picture.update(
        status=True,
    )

@usersapp.post('/change_access_func/{google_id}')
async def change_asses_func(google_id:str,day_limit: Optional[int] = 5, status:Optional[bool]= True):
    user = await Users.objects.get_or_none(id_google_client=google_id)
    return await user.update(access=status,day_limit=day_limit)
  



@usersapp.delete('/{id}')
async def delete_user(google_id:str):
    user = await Users.objects.get_or_none(id_google_client=google_id)
    return await user.delete()

@usersapp.post('/ddd/{id}')
async def ddddddelete_user(google_id:str):
    user = await Users.objects.all()
    return user


    


   
