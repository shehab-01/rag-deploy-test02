import json
import hmac
import base64
from typing import Union
from typing_extensions import Annotated
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.config import Config

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

from api.utils.logger import logger
from api.common import config, consts
from api.common import exceptions as ex
from api.service import user_service
from api.model.models import User, UserData, fake_db_users

# config = Config(".env")
# JWT_ALGORITHM = config("JWT_ALGORITHM")
# JWT_SECRET_KEY = config("JWT_SECRET_KEY")
# JWT_EXPIRE_MINUTES = int(config("JWT_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")
# print("pwd_context:", pwd_context.hash("1122"))


class Token(BaseModel):
    token_type: Union[str, None] = None
    access_token: Union[str, None] = None


class TokenData(Token):
    username: Union[str, None] = None


class TokenHelper:
    def __init__(self):
        pass

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return pwd_context.hash(password)

    def get_user(username: str) -> User:
        user_data = TokenHelper.get_user_data(username)
        user_dict = user_data.dict()
        return User(**user_dict)

    def get_user_data(username: str) -> UserData:
        # TODO: DB 세팅후 조회로 변경
        # db = fake_db_users
        # if username in db:
        #     user_dict = db[username]
        #     return UserData(**user_dict)

        user_view = user_service.user_view(dict(user_id=username))
        return UserData(**user_view)

    def authenticate_user(username: str, password: str) -> User:
        user_data = TokenHelper.get_user_data(username)
        if not user_data:
            return False
        if not TokenHelper.verify_password(password, user_data.user_pw):
            return False
        return user_data

    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=consts.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, consts.JWT_SECRET, algorithm=consts.JWT_ALGORITHM)
        return encoded_jwt

    async def token_decode(access_token: str) -> dict:
        try:
            access_token = access_token.replace("Bearer ", "")
            payload = jwt.decode(access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
        except ExpiredSignatureError:
            raise ex.TokenExpiredEx()
        except JWTError:
            raise ex.TokenDecodeEx()
        return payload

    async def get_curr_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )  # fmt: skip
        try:
            # payload = jwt.decode(token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM])
            payload: dict = await TokenHelper.token_decode(token)
            username: str = payload.get("sub")
            if username is None:
                raise ex.TokenCredentialEx()

            token_data = TokenData(username=username)
            user = TokenHelper.get_user(username=token_data.username)
            if user is None:
                raise ex.TokenCredentialEx()
        except Exception:
            # raise credentials_exception
            raise ex.TokenCredentialEx()
        return user

    async def user(user: Annotated[User, Depends(get_curr_user)]) -> User:
        if user.use_yn != "Y":
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
