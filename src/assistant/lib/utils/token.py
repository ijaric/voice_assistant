import fastapi
import fastapi.security
import jose
import jose.jwt
import pydantic

import lib.app.settings as app_settings
import lib.models as models


def get_token_data(
    authorization: fastapi.security.HTTPAuthorizationCredentials = fastapi.Security(fastapi.security.HTTPBearer()),
) -> models.Token:
    settings = app_settings.Settings()

    token = authorization.credentials
    try:
        secret_key = settings.project.jwt_secret_key
        payload = jose.jwt.decode(token, secret_key, algorithms=[settings.project.jwt_algorithm])
        return models.Token(**payload)
    except (jose.JWTError, pydantic.ValidationError) as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from error
