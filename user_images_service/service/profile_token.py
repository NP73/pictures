from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from jose import JWTError, jwt

from config.settings  import settings
from repositories.users import Users


ACCESS_TOKEN_EXPIRE_MINUTES = 60

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTBearer(HTTPBearer):

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