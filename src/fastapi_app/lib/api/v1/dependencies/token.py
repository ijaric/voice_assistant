import fastapi
from jose import JWTError, jwt
from pydantic import ValidationError

import lib.api.schemas as app_schemas


def get_token_data(
    request: fastapi.Request,
    authorization: fastapi.security.HTTPAuthorizationCredentials = fastapi.Security(fastapi.security.HTTPBearer()),
) -> app_schemas.entity.Token:
    token = authorization.credentials
    settings = request.app.state.settings
    try:
        secret_key = settings.jwt_secret_key
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return app_schemas.entity.Token(**payload)
    except (JWTError, ValidationError):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
