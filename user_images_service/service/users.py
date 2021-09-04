from repositories.users import Users
from datetime import datetime


from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .pictures import get_status_upload_image,save_origin_image





async def date_time_count(last_picture_user_time):

    """
    Сравнивает время в данный момент с временем
    последнего загруженного изображения, 
    возвращает результат в минутах
    """

    time_pict  = datetime.strptime(str(last_picture_user_time), "%Y-%m-%d %H:%M:%S.%f")
    now_date_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    print(str(datetime.now()), str(last_picture_user_time))
    now = str(datetime.now())[5:7]
    pict = str(last_picture_user_time)[5:7]
    print(int(now)-int(pict))
    return int((now_date_time - time_pict).seconds/60)

async def date_time_count_day(last_picture_user_time):

    """
    Сравнивает время в данный момент с временем
    последнего загруженного изображения, 
    возвращает результат в минутах
    """
    print('day')
    now = str(datetime.now())[5:7]
    pict = str(last_picture_user_time)[5:7]
    return int(now)-int(pict)
    


async def user_data_upload(user_google_id,image,task):

    """
    В функции идет проверка прошло ли 24 часа с
       загрузки последнего изображения - если да ,то обнуляется лимит на 0 в поле 
       таблицы Users **spent_day_limit** и передается выполнение функции
       save_origin_image в папке service в файле pictures 
    Также идет проверка на время загрузки последнего изображения в функции
      , если прошло более 30 минут , а статус в поле **status**
      таблицы Pictures все еще False, то идет обновление этого поля на True , 
      что бы пользователь мог снова загружать изображения 
      и передается выполнение функции
      save_origin_image в папке service в файле pictures 
      В случае соответствия лимита на загрузку изображений возвращает
      message =Успех и status = True
      В случае несоответсвия возвращает status False и соответсвующее сообщение о причинах 
      записанное в message

    """
    
    user = await Users.objects.get_or_none(id_google_client=user_google_id)
    last_picture_user = await get_status_upload_image(user.last_uploaded_image_id)
    message = 'Успешно'
    status = True
    if not user.access:
        message = 'У вас нет доступа к функции сервиса'
        status = False
    elif user.spent_day_limit >= user.day_limit:
        print(await date_time_count(last_picture_user.timestamp))
        if await date_time_count_day(last_picture_user.timestamp) > 1:
            timestamp,id_image = await save_origin_image(user_google_id, image,task)
            await user.update(
                last_uploaded_image_id = id_image,
                spent_day_limit = 1,
                last_timestamp_image = timestamp
            )
            status = True
            message = 'Успешно'
        else:
            message = 'Вы исчерпали дневной лимит'
            status = False
    elif user.last_uploaded_image_id:
        
        
        if not last_picture_user.status:
            if await date_time_count(last_picture_user.timestamp) > 30:
                timestamp,id_image = await save_origin_image(user_google_id, image,task)
                await user.update(
                last_uploaded_image_id = id_image,
                spent_day_limit = user.spent_day_limit + 1,
                last_timestamp_image = timestamp
                )
                status = True
                message = 'Успешно'
            else:
                message = 'Дождитесь обработки изображения'
                status = False
        else:
            timestamp,id_image = await save_origin_image(user_google_id, image,task)
            await user.update(
            last_uploaded_image_id = id_image,
            spent_day_limit = user.spent_day_limit + 1,
            last_timestamp_image = timestamp
                )
            status = True
            message = 'Успешно'
    else:
        timestamp,id_image = await save_origin_image(user_google_id, image,task)
        await user.update(
                last_uploaded_image_id = id_image,
                spent_day_limit = user.spent_day_limit + 1,
                last_timestamp_image = timestamp
                )
    content = {"message": message ,
            "status": status,
            "user_data": user
            }
    json_compatible_item_data = jsonable_encoder(content)
    return JSONResponse(
        status_code=200,
        content=json_compatible_item_data
    )






