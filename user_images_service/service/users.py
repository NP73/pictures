from repositories.users import Users
from datetime import datetime


from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .pictures import get_status_upload_image,save_origin_image





async def date_time_count(last_picture_user_time):
   
    
    time_pict  = datetime.strptime(str(last_picture_user_time), "%Y-%m-%d %H:%M:%S.%f")
    now_date_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    return int((now_date_time - time_pict).seconds/60)


async def user_data_upload(user_google_id,image,task):
    user = await Users.objects.get_or_none(id_google_client=user_google_id)
    last_picture_user = await get_status_upload_image(user.last_uploaded_image_id)
    message = 'Успешно'
    status = True
    if not user.access:
        print(1)
        message = 'У вас нет доступа к функции сервиса'
        status = False
    elif user.spent_day_limit >= user.day_limit:
        print(2)
        if await date_time_count(last_picture_user.timestamp) > 1440:
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
            print(3)
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
                print(10)
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
        print(5)
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






