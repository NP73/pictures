from repositories.users import Users
from datetime import datetime





async def get_time_left(date_time, user):
    today_data_time = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    if (int(date_time[:2]) - int(today_data_time[:2])) >= 1:

        if(int(date_time[11:13]) >= int(date_time[11:13])):
            await user.update(spent_day_limit = 0, access = 0)
            return True,user.spent_day_limit
            
    else:
        return False, user.spent_day_limit


async def get_count_images_user_id(user_id):
    user = await Users.objects.get_or_none(id_google_client=user_id)
    if user.spent_day_limit == 5:
        return await get_time_left(user.last_timestamp, user)
    else:
        await user.update(
            access = 0,
            spent_day_limit = user.spent_day_limit + 1,
            last_timestamp = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            )
        return True,user.spent_day_limit




