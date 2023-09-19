import fastapi

from jose import JWTError, jwt
from pydantic import ValidationError

from lib.api import schemas as app_schemas
from lib.app import settings as app_settings

app = fastapi.FastAPI()
settings = app_settings.get_settings()

security = fastapi.security.HTTPBearer()


def get_token_data(
    authorization: fastapi.security.HTTPAuthorizationCredentials = fastapi.Security(security),
) -> app_schemas.entity.Token:
    token = authorization.credentials
    try:
        secret_key = settings.jwt_secret_key
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return app_schemas.entity.Token(**payload)
    except (JWTError, ValidationError):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
