from typing import Optional
from datetime import timedelta
from datetime import datetime


from jose import jwt

from repositories.users import Users
from config.settings import settings


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


class UserClient():

    """
    класс для создания и верефикации пользователя
    по JWT токену
    """

    async def create_access_token(
        self,
        id_google_client: str,
        expires_delta: Optional[timedelta] = None
    ):

        """
        Создает JWT токен из id пользователя
        и назначает его время жизни
        """
        
        to_encode = id_google_client.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update(
            {"exp": expire}
        )
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=ALGORITHM)
        return encoded_jwt

    async def token_id(self, id_google_client):

        """
        Принимает id пользователя 
        и создает его hash JWT 
        """

        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = await self.create_access_token(
            {"sub": str(id_google_client)},
            expires_delta=access_token_expires
        )
        return access_token, access_token_expires

    async def virefity_profile(
        self,
        user_data
    ):

        """
        Проверяет есть ли такой пользователь,
        если нету ,тогда создает нового
        передает id_google_client в функцию хеширования
        token_id()
        """

        user_get = await Users.objects.get_or_none(id_google_client=user_data.id_google_client)
        if not user_get:
            user = await Users.objects.create(**user_data.dict())
        else:
            user = user_get
        return await self.token_id(user.id_google_client)


user_service = UserClient()
