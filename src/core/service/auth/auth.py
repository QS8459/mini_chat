import jwt
from jwt.exceptions import InvalidTokenError, InvalidSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.conf.settings import settings
from src.conf.loging import log

from src.core.service.account.account import AccountService, get_account_service
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/account/login/', scheme_name='jwt')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    acc_service: AccountService = Depends(get_account_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, settings.token_crypt_algorithm)
        username = payload.get('username')
        if username is None:
            raise credentials_exception
        exp_date = payload.get('exp')
        time_diff = (datetime.now(timezone.utc).timestamp() - exp_date) / 60
        if 0 < time_diff < 30:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token Expired',
                headers={"WWW-Authenticate": "Bearer"}
            )
        user = await acc_service.get_by_email(username)
        return user
    except (InvalidTokenError, InvalidSignatureError) as e:
        log.error(e)

        raise credentials_exception


def generate_token(data: dict = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_exp_time_min)
    to_encode.update({'exp': expire})

    return jwt.encode(
        payload=to_encode,
        key=settings.secret_key,
        algorithm=settings.token_crypt_algorithm
    )

