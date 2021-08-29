import ast
import time
import asyncio
import threading
import queue
import random
from typing import Optional

import os
import shutil

from fastapi.encoders import jsonable_encoder
import numpy as np
import matplotlib.pyplot as plt
import cv2


from routers.socket_route import list_user_id_socket, manager
from repositories.pictures import Pictures



hosts = 'api-booking.ru:8000'
queue_task = queue.Queue()


async def add_alert_brayzer_client(
        img_link_origin,
        origin_img_id,
        user_google_id: str,
        result_dict,
        image: Optional[str] = None):
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
                 }
            ), user_connect['websocket_client'])
        else:
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
    else:
        pass

    return 'ok'


async def image_change(user_google_id, img_origin_path, result_path, origin_img_id, dict: Optional[dict] = {}):
    image = cv2.imread(img_origin_path)
    dict['a'] = 10
    size_image = np.copy(image[..., 0:3])  # убираем лишнюю размерность
    k = dict['a']  # количество выходных картинок
    for i in range(k):
        img_i = size_image*int(i/k+1)
        # рисунки сохраняются в одну папку
        plt.imsave(f'{result_path}/{str(i)}return.png', img_i)
        time.sleep(15)
        await add_alert_brayzer_client(
            img_link_origin=f'http://{hosts}/{img_origin_path}',
            origin_img_id=origin_img_id,
            user_google_id=user_google_id,
            result_dict=None,
            image=f'http://{hosts}/{result_path}/{str(i)}return.png'
        )
        
        # тут более-менее реальное время обработки функции, работаем над умешьшением
        time.sleep(3)
    result_dict = dict
    status = 1
    print(result_dict, status)
    await add_alert_brayzer_client(
        img_link_origin=f'http://{hosts}/{img_origin_path}',
        origin_img_id=origin_img_id,
        user_google_id=user_google_id,
        result_dict=result_dict,
        image=''

    )
    # возвращается выходной словарь и сигнал о завершении работы функции
    return result_dict, status


async def upload_images():
    len_task_item = queue_task.qsize()
    while len_task_item:
        client = queue_task.get()
        print(
            f'добавлено изображение на обработку от клиента с id {client[0]},image:{client[1]}')
        user_google_id = client[0]
        image_origin_path = client[1]
        result_path = client[2]
        origin_img_id = client[3]
        await image_change(user_google_id, image_origin_path, result_path, origin_img_id, dict={})
        queue_task.task_done()
        len_task_item = queue_task.qsize()


def start_thread_upload():
    print('start_thread_upload')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(upload_images())
    loop.close()


async def apend_item_quene(user_google_id, image_origin_path, result_path, origin_img_id):
    queue_task.put([user_google_id, image_origin_path,
                   result_path, origin_img_id])
    print(threading.active_count())
    try:
        if threading.active_count() == 8:
            print('thread = 8')
            pass
        if threading.active_count() < 8:
            print('thread < 8')
            threading.Thread(target=start_thread_upload, args=()).start()
    except:
        pass


async def save_origin_image(user_google_id, image):

    path_dir = '/usr/src/app/static/images'
    if not os.path.exists(f'{path_dir}/{user_google_id}'):
        os.mkdir(f'{path_dir}/{user_google_id}')

    if not os.path.exists(f'{path_dir}/{user_google_id}/{image.filename}'):
        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}')
        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}/origin')
        os.mkdir(f'{path_dir}/{user_google_id}/{image.filename}/result')
    with open(f"{path_dir}/{user_google_id}/{image.filename}/origin/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        image_link = f'http://{hosts}/{path_dir}/{user_google_id}/{image.filename}/origin/{image.filename}'
    new_image = await Pictures.objects.create(
        user_id_google=user_google_id,
        img_link=image_link,
        settings=str({'a': 10}),
        status=False,
        result_imgs_link=str({}),
        result_dict=str({}),
    )

    result_img_path = f'{path_dir}/{user_google_id}/{image.filename}/result'
    await apend_item_quene(user_google_id, image_link[22:], result_img_path, new_image.id)


async def reverse_dict_for_str_picture(picture):
    picture.result_imgs_link = str(picture.result_imgs_link)
    picture.result_dict = str(picture.result_dict)
    picture.settings = str(picture.settings)
    return picture


async def reverse_str_for_dict_picture(picture):
    picture = picture.dict()
    picture['result_imgs_link'] = ast.literal_eval(picture['result_imgs_link'])
    picture['result_dict'] = ast.literal_eval(picture['result_dict'])
    picture['settings'] = ast.literal_eval(picture['settings'])
    return [picture]

queue_task.join()
