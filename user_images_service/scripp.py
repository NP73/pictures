import numpy as np
import matplotlib.pyplot as plt
import random
from typing import Optional
import time
import cv2

image= cv2.imread('static/images/117617572761444892107.jpg')



def image_change(img, dict:Optional[dict] = {}):
    image = cv2.imread(img)
    dict['a'] = 10
    img1 = np.copy(img[..., 0:3]) # убираем лишнюю размерность  
    k = dict['a'] # количество выходных картинок
    for i in range(k):
        print('jjj')
        # time.sleep(5+random.random()*20) #тут более-менее реальное время обработки функции, работаем над умешьшением
        img_i = img1*i/k
        plt.imsave(f'{str(i)}return.png', img_i) # рисунки сохраняются в одну папку
    result_dict = dict
    status = 1
    print(result_dict,status)
    return result_dict, status #возвращается выходной словарь и сигнал о завершении работы функции

image_change(image)

