from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from repositories.users import Users
from repositories.pictures import Pictures
from schemas import users
from service import userauth


usersapp = APIRouter(
    prefix="/api/v1/users",
    responses={404: {"description": "Not found"}}
)


@usersapp.post('/')
async def create(user_data: users.UserCreate):

    """
     Функция создает нового пользователя  , 
    - **id_google_client**   id пользователя google
    - **email**- email пользователя гугл
    - **password**- пароль пользователя,необязательое поле
    - **access**- разрешен ли пользователю доступ к основной функции
      по умольчанию разрешен - True
    - **spent_day_limit**- счетчик изображений пользователя ,изначально 0
    - Возвращает токен - поле **access_token**
    - Возвращает время действия токена в секундах - поле **access_token_expires**
    - Возвращает созданного пользователя - поле **access_token_expires**
    """

    access_token, access_token_expires = await userauth.user_service.virefity_profile(
        user_data
    )
    user = await Users.objects.get_or_none(id_google_client=user_data.id_google_client)

    cont = {"access_token": access_token,
            "access_token_expires": access_token_expires,
            "user_data": user, }
    json_compatible_item_data = jsonable_encoder(cont)
    return JSONResponse(
        status_code=200,
        content=json_compatible_item_data
    )


@usersapp.post('/token')
async def create_token(google_user_id: int):

    """
     Функция создает JWT  токен по полю таблицы **id_google_client** , 
    - Возвращает токен и его время действия в секундах
    """

    access_token, access_token_expires = await userauth.user_service.token_id(
        google_user_id
    )

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

    """
     Функция возвращает всех пользователей
    """

    return await Users.objects.all()


@usersapp.get('/{id_google}')
async def get_one(id_google: int):

    """
     Функция возвращает одного пользователя, 
     если пользователя с таким id нет возвращает null
     
     - **id_google**: id гугл пользователя
    """

    return await Users.objects.get_or_none(id_google_client=id_google)


@usersapp.post('/change_status/{id_google_client}')
async def update_status_user(id_google_client: str):

    """
     Функция меняет статус обработки изображения по завершению
     и добавляет в поле  **result_dict** изначальные настройки
     изображения которые были в поле таблицы  Pictures **settings**
     - если пользователя с таким id нет возвращает null 
     - **id_google**: id гугл пользователя
    """

    user = await Users.objects.get_or_none(id_google_client=id_google_client)
    picture = await Pictures.objects.get_or_none(
        id=user.last_uploaded_image_id
    )
    return await picture.update(
        status=True,
        result_dict=picture.settings
    )


@usersapp.post('/change_access_func/{google_id}')
async def change_asses_func(
    google_id: str,
    day_limit: Optional[int] = 5,
    status: Optional[bool] = True
    ):

    """
    Функция для администраторов сервиса
    - **access** Меняет статус доступа пользователя
      к основной функции обработки изображения
      **True** - доступ разрешен , **False** - доступ запрещен
    - **day_limit** Изменяет дневной лимит на загрузку изображений
                                             в поле **day_limit**
    """

    user = await Users.objects.get_or_none(
        id_google_client=google_id
    )
    return await user.update(
        access=status, day_limit=day_limit
    )


@usersapp.delete('/{id}')
async def delete_user(google_id: str):

    """
    Функция удаляет пользователя по **id_google_client**
    - **id_google_client** поле таблицы пользователя id_google_client
    """
    
    user = await Users.objects.get_or_none(id_google_client=google_id)
    return await user.delete()
