import ormar
import datetime


from config.database import metadata, database


class Users(ormar.Model):

    """
    id - id пользователя

    email - email пользователя

    password - HASH пароля пользователя

    access- разрешен ли пользователю доступ к основной функции

    spent_day_limit - сколько израсходовано из суточного лимита
    
                   загрузки изображений максимальное значение 5
      изначально поле spent_day_limit=0, при добавлении изображения, к числу поля 
      прибавляется +1 и записывается дата и время добавления каждого изображения - create_at. 
      при добавлении идет проверка : проверяется количество добавленных изображений
      в счетчике нашего поля , если в счетчике нашего поля число больше 0 но меньше 5 , 
      тогда идет сверка сегодняшней даты с датой последней удачной загрузки изображения
      last_timestamp:
    - 1.если даты равны, тогда система разрешает загрузку изображений до 5
    - 2.если даты не равны(допустим загрузка изображения была вчера или позавчера) и
      счетчик равен 1 или 2,3,4,5 , тогда при загрузке изображения уже сегодня предварительно 
      счетчик обнуляеться до числа 0 и  идет загрузка нового изображения и после чего уже 
      в обновленный счетчик добавляется 1 и в последующем соблюдается пункт 1

    last_timestamp - дата и время  последней удачной загрузки картинки

    """

    class Meta:
        tablename = "users_table"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=255, null=True)
    password: str = ormar.String(max_length=1000, null=True)
    access:bool = ormar.Boolean(default=False)
    spent_day_limit: int = ormar.Integer(maximum=5,default=0)
    last_timestamp: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)


    

    class Config:
        orm_mode = True

        


