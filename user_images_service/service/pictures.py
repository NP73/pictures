import ast
import time


async def reverse_dict_for_str_picture(picture):
    picture.result_imgs_link = str(picture.result_imgs_link)
    picture.result_dict = str(picture.result_dict)
    return picture


async def reverse_str_for_dict_picture(picture):
    picture = picture.dict()
    picture['result_imgs_link'] = ast.literal_eval(picture['result_imgs_link'] )
    picture['result_dict'] = ast.literal_eval(picture['result_dict'])
    return [picture]


def logics_image(image):
    num = 0
    while num <3:
        print('что то делаеться с картинкой')
        time.sleep(5)
        num += 1
        
    print('готово')

