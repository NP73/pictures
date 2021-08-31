from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from jose import JWTError, jwt

from config.settings  import settings



ACCESS_TOKEN_EXPIRE_MINUTES = 60 # время жизни токена в минутах

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTBearer(HTTPBearer):

    """
    Класс верефикации действительности токена по
    id_google пользователя
    """

    def __init__(
        self,
        auto_error: bool = True
        ):
        super(
            JWTBearer,
            self).__init__(
            auto_error=auto_error
            )

    async def __call__(

        self, request: Request
        ):

        """
        Проверяет есть ли такой токен в базе токенов
        """

        credentials: HTTPAuthorizationCredentials = await super(
                            JWTBearer, self
                            ).__call__(
                                request
                                )
        
        if credentials:
            return await self.get_current_user(credentials.credentials)
   

    async def get_current_user(
        self,
        token: str 
        ):

        """
        Принимает токен и конвертирует его в данные пользователя
        """
        
        try:
            payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM])
            id_client = payload.get(
            "sub"
            )
            return id_client
        
        except JWTError:
            return JWTError