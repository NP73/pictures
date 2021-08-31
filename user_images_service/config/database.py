import databases
import sqlalchemy


from .settings import settings


# URL_DATA_BASE = 'postgresql://gleb:postgres1@localhost/image'

URL_DATA_BASE  = (
                'postgresql://'
                f'{settings.postgres_user}:'
                f'{settings.postgres_password}'
                '@basedata:5432/'
                f'{settings.postgres_db}'
                )
# database - асинхронное подключение к базе данных
database = databases.Database(URL_DATA_BASE)
# engine - создать таблицы в базе данных если они не созданы
engine = sqlalchemy.create_engine(URL_DATA_BASE)
# metadata - вся информация из таблиц
metadata = sqlalchemy.MetaData()
