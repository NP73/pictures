import ast
import time
import asyncio
import threading
import queue
import requests
from typing import Optional
import json

import os
import shutil

from fastapi.encoders import jsonable_encoder
from fastapi import WebSocketDisconnect
import numpy as np
import matplotlib.pyplot as plt
import cv2


from routers.socket_route import list_user_id_socket, manager
from repositories.pictures import Pictures



headers = {
    "Content-Type": "application/json",
}
# hosts = 'localhost:8000'
hosts = 'api-booking.ru:8000'


async def add_alert_brayzer_client(
        img_link_origin,
        origin_img_id,
        user_google_id: str,
        result_dict,
        count_res_image,
        image: Optional[str] = None):

    """
    Функция отправки статуса обработки
    и только что созданных результирующих изображений 
    клиенту в браузер 

    Работает на вебсокетах!)
    """
    
    if (user_google_id in [user_id['user_google_id']
                           for user_id in
                           list_user_id_socket]
        ):
        user_connect = ([
            user_data for user_data in list_user_id_socket
            if user_data['user_google_id'] == user_google_id
        ][0])
        if image:
            await manager.send_personal_message(jsonable_encoder(
                {'close_result': False,
                 'origin_img_id': origin_img_id,
                 'img_link_origin': img_link_origin,
                 'result_image': image,
                 'user_google_id': user_google_id,
                 'result_dict': result_dict,
                 'count_res_image': count_res_image
                 }
            ), user_connect['websocket_client'])
        else:
            try:
                await manager.send_personal_message(jsonable_encoder(
                    {
                        'close_result': True,
                        'origin_img_id': origin_img_id,
                        'img_link_origin': img_link_origin,
                        'result_image': None,
                        'user_google_id': user_google_id,
                        'result_dict': result_dict,
                    }
                ), user_connect['websocket_client'])
            except WebSocketDisconnect:
                manager.disconnect(user_connect['websocket_client'])
    else:
        pass

    return 'ok'


async def send_link_image(result_path,img_origin_path,origin_img_id,user_google_id,i):
    """
    1 - передает серверу ,
    что обработано изображение и есть результирующее
    изображение,сервер его сохраняет(функция выполнения папка routes
    файл pictures  функция  add_result_img_link_for_origin)
    2 - передает данные в функцию add_alert_brayzer_client
    для отправки данных по вебсокетам
    """
    image = f'http://{hosts}/{result_path}/{str(i)}return.png',
    url = f'http://localhost:8000/api/v1/pictures/add_link_img/{origin_img_id}'
    data = {
        "img_link": f'http://{hosts}/{result_path}/{str(i)}return.png'
    }
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    count_link = res.json()
    await add_alert_brayzer_client(
        img_link_origin=f'http://{hosts}/{img_origin_path}',
        origin_img_id=origin_img_id,
        user_google_id=user_google_id,
        result_dict=None,
        count_res_image=count_link['count_res_image'],
        image=f'http://{hosts}/{result_path}/{str(i)}return.png',

    )

async def send_result_client(img_origin_path,origin_img_id,user_google_id,result_dict):

    """
    1 - передает серверу ,
    что обработка изображения закончена 
    сервер сохраняет данные и ставит статус в Pictures оригинального изображения 
    status = True
    (функция выполнения папка routes
    файл users  функция  add_result_img_link_for_origin)
    2 - передает данные в функцию update_status_user
    для отправки данных по вебсокетам
    """

    requests.post(
        f'http://localhost:8000/api/v1/users/change_status/{user_google_id}',
    )
    await add_alert_brayzer_client(
        img_link_origin=f'http://{hosts}/{img_origin_path}',
        origin_img_id=origin_img_id,
        user_google_id=user_google_id,
        result_dict=result_dict,
        count_res_image=10,
        image=''
    )

async def image_change(user_google_id, img_origin_path, result_path, origin_img_id, dict: Optional[dict] = {}):
    """
    функция обработчик изображений 
    """
    image = cv2.imread(img_origin_path)
    dict['a'] = 10
    size_image = np.copy(image[..., 0:3])  # убираем лишнюю размерность
    k = dict['a']  # количество выходных картинок
    for i in range(k):
        img_i = size_image*int(i/k+1)
        # рисунки сохраняются в одну папку
        plt.imsave(f'{result_path}/{str(i)}return.png', img_i)
        time.sleep(5)

        """
        send_link_image - передает серверу ,
        что обработано изображение и есть результирующее
        изображение
        """

        await send_link_image(result_path,img_origin_path,origin_img_id,user_google_id,i)
        # тут более-менее реальное время обработки функции, работаем над умешьшением
    result_dict = dict
    status = 1

    """
    send_result_client - передает серверу ,что обработка закончена
    """
    await send_result_client(img_origin_path,origin_img_id,user_google_id,result_dict)
    # возвращается выходной словарь и сигнал о завершении работы функции
    return result_dict, status


async def upload_images(user_google_id, image_origin_path, result_path, origin_img_id):

    """
    отправляет данные функции обработчику изображений  - image_change
    """

    user_google_id = user_google_id
    image_origin_path = image_origin_path
    result_path = result_path
    origin_img_id = origin_img_id
    await image_change(user_google_id, image_origin_path, result_path, origin_img_id, dict={})



def for_async(user_google_id, image_origin_path, result_path, origin_img_id):

    """
    передает из потока функцию для ее асинхронного выполнения
    """

    asyncio.run(upload_images(user_google_id,
                image_origin_path, result_path, origin_img_id))





async def save_origin_image(user_google_id, image, task):

    """
    сохраняет изображение и создает под них папки по соответсвию
    - папка origin -под оригинальное изображение
    - папка result - под результирующее изображение
    все изображения сохраняються в каталоге static/images
    """

    path_dir = 'static/images'
    if not os.path.exists(f'{path_dir}/{user_google_id}'):

        """
        Если такого пути еще нет создается папка которая соответсвует(ее название)
        google id пользователя
        """

        os.mkdir(f'{path_dir}/{user_google_id}')

    if not os.path.exists(f'{path_dir}/{user_google_id}/{image.filename}'):

        """
        создается папка origin и result,(если их еще нет)
        в папке которая соответсвует(ее название)
        google id пользователя 
        """

        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}')
        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}/origin')
        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}/result')
    with open(f"{path_dir}/{user_google_id}/{image.filename}/origin/{image.filename}", "wb") as buffer:
        
        """
        сохраняет изображение в созданные выше папки
        """

        shutil.copyfileobj(image.file, buffer)
        image_link = f'http://{hosts}/{path_dir}/{user_google_id}/{image.filename}/origin/{image.filename}'
    
    """
    Pictures.objects.create - сохраняет изображение

    """

    new_image = await Pictures.objects.create(
        user_id_google=user_google_id,
        img_link=image_link,
        settings=str({'a': 10}),
        status=False,
        result_imgs_link=str({}),
        result_dict=str({'a': 0}),
    )
    image_link = f'{path_dir}/{user_google_id}/{image.filename}/origin/{image.filename}'
    result_img_path = f'{path_dir}/{user_google_id}/{image.filename}/result'
    
    """
    task.add_task -передает обработку сохраненного изображения в отельный поток

    """

    task.add_task(for_async, user_google_id, image_link,
                  result_img_path, new_image.id)
    return new_image.timestamp, new_image.id


async def reverse_dict_for_str_picture(picture):

    """
    Конвертирует словарь в строку  
    """

    picture.result_imgs_link = str(picture.result_imgs_link)
    picture.result_dict = str(picture.result_dict)
    picture.settings = str(picture.settings)
    return picture


async def reverse_str_for_dict_picture(picture):

    """
    Конвертирует строку в словарь
    """

    picture = picture.dict()
    picture['result_imgs_link'] = ast.literal_eval(picture['result_imgs_link'])
    picture['result_dict'] = ast.literal_eval(picture['result_dict'])
    picture['settings'] = ast.literal_eval(picture['settings'])
    return [picture]


async def get_status_upload_image(image_id):

    """
    Возвращает статус обработки изображени
    """

    picture = await Pictures.objects.get_or_none(id=image_id)
    return picture
