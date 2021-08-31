from repositories.users import Users
import ast


from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Depends,
    BackgroundTasks
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

    """
     Функция создает новое Изображение, 
    - **id_google_client** id пользователя google который добавил изображение
    - **img_link**- ссылка на сохраненное изображение
    - **settings**- словарь настроек изображения по умолчанию {'a':10}
    - **status**- статус обработки изображения (
        во время обработки False,по завершению True
        )
    - **result_dict** - результат настроек по умолчанию пуст,после обработки 
        изображения добавляется словарь из изночальных настроек

    - Возвращает созданное изображение
    """

    picture_dict = await reverse_dict_for_str_picture(
        picture
    )
    return await Pictures.objects.create(**picture_dict.dict())


@pictureapp.get('/')
async def get_all():

    """
     Функция возвращает все Изображения
    """

    return await Pictures.objects.all()


@pictureapp.get('/{id}')
async def get_one(id: int):

    """
     Функция возвращает изображение по его id
    """

    picture = await Pictures.objects.get_or_none(id=id)
    return await reverse_str_for_dict_picture(picture)


@pictureapp.get('/status-image-process/pred')
async def status_image_upload(curent_user=Depends(
    profile_token.JWTBearer())
):

    """
    Просмотр статуса обработки изображения
    - **curent_user** - JWT токен авторизации
    - Если пользователь не авторизован - возвращает 
     сообщение: выполните вход
    - Если у пользователя нет еще изображений - возвращает 
     сообщение: У вас нет изображений
    """

    if type(curent_user) != str:
        return JSONResponse(
            status_code=400,
            content={
                "status": "badd",
                "detail": "Выполните вход",
            },
        )
    else:
        user = await Users.objects.get_or_none(
            id_google_client=curent_user
        )
        picture = await Pictures.objects.get_or_none(
            id=user.last_uploaded_image_id
        )
        if not picture:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "badd",
                    "detail": "У вас нет изображений",
                }
            )
        else:
            return await reverse_str_for_dict_picture(picture)


@pictureapp.post('/add_link_img/{id_img_origin}')
async def add_result_img_link_for_origin(
    id_img_origin: int, link_image: pictures.LinkImage
):

    """
    Функция добавляет ссылки на результирующие изображения
    в словарь поля **result_imgs_link** и после каждого этапа обработки 
        добавляет в словарь result dict количество уже пройденных этапов
    - **id_img_origin** - id оригинального изображения
    - **link_image** -ссылка на рузультирующее изображение из функции
     обработчика после его сохранения в папке

    - Возвращает количество добавленных результирующих изображений
     и все ссылки на готовые результирующие изображения 

    - к этой функции обращается функция обработчик изображений
      находиться в папке service файл pictures называется
      **send_link_image**

    """

    picture = await Pictures.objects.get_or_none(id=id_img_origin)
    result_linc = ast.literal_eval(picture.result_imgs_link)
    result_dict = ast.literal_eval(picture.result_dict)
    
    result_dict['a'] = result_dict['a']+1
    result_linc[str(len(result_linc)+1)] = link_image.img_link

    await picture.update(
        result_imgs_link=str(result_linc),
        result_dict = str(result_dict)
    )

    return {
        'result_imgs_link': link_image.img_link,
        'count_res_image': len(result_linc)
    }


@pictureapp.post("/uploadimages/{user_google_id}")
async def create_upload_file(
    user_google_id: str,
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...)
):

    """
    Функция добавляет изображение для обработки 
    - **user_google_id** - id  пользователя гугл
    - **image** - файл изображения
    - передает управление функции user_data_upload, 
     которая проверяет есть ли лимт у пользователя
     по загруженным изображениям за день и находиться
     ли предыдущее загруженное изображение в статусе обработки
     - В случае успеха сохраняет изображение и передает выполнение
      в отдельном потоке функции обработчику **image_change**
      если лимит исчерпан или загрузка предыдущего изображения не закончена 
      возвращает соответсвующий ответ пользователю 
       В функции user_data_upload также идет проверка прошло ли 24 часа с
       загрузки последнего изображения - если да ,то обнуляется лимит на 0 в поле 
       таблицы Users **spent_day_limit**
    - Также идет проверка на время загрузки последенего изображения в функции
      user_data_upload , если прошло более 30 минут , а статус в поле **status**
      таблицы Pictures все еще False, то идет обновление этого поля на True , 
      что бы пользователь мог снова загружать изображения

    """
    
    return await users.user_data_upload(user_google_id, image, background_tasks)
