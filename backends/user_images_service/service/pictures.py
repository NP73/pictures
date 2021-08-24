import ast


async def reverse_dict_for_str_picture(picture):
    picture.result_imgs_link = str(picture.result_imgs_link)
    picture.result_dict = str(picture.result_dict)
    return picture


async def reverse_str_for_dict_picture(picture):
    picture = picture.dict()
    picture['result_imgs_link'] = ast.literal_eval(picture['result_imgs_link'] )
    picture['result_dict'] = ast.literal_eval(picture['result_dict'])
    return [picture]