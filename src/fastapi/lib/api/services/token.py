from jose import JWTError, jwt
from pydantic import ValidationError

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from lib.api.schemas.entity import Token
from lib.app import settings as lib_app_settings

app = FastAPI()
settings = lib_app_settings.get_settings()

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
