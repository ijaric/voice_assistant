from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from libs.api.schemas.entity import Token
from libs.app import settings as libs_app_settings
from pydantic import ValidationError

app = FastAPI()
settings = libs_app_settings.get_settings()

security = HTTPBearer()


def get_token_data(
    authorization: HTTPAuthorizationCredentials = Security(security),
) -> Token:
    token = authorization.credentials
    try:
        secret_key = settings.jwt_secret_key
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return Token(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

