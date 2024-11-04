from fastapi import status
from typing import Union, Optional
from pydantic import BaseModel, ValidationError


class Error(BaseModel):
    code: Optional[str] = None
    type: Optional[str] = None
    detail: Optional[str] = None


class ErrData(BaseModel):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    msg: Optional[str] = None
    error: Optional[Error] = None


class ResData(BaseModel):
    status: int = status.HTTP_200_OK
    msg: Optional[str] = None
    data: Optional[object] = None


class User(BaseModel):
    user_id: str
    user_nm: str
    user_type: str
    email: Optional[str] = None
    telno: Optional[str] = None
    use_yn: str


class UserData(User):
    user_pw: Optional[str]


fake_db_users = {
    "admin": {
        "username": "admin",
        "full_name": "어드민",
        "email": "admin@maxdata.kr",
        "hashed_password": "$2b$12$16OwQZ31e2Ds/2ELoVCqgudzXZdG5VKd9AmNzMKq9dk2rZI.5rJRC",
        "disabled": False,
    },
    "test": {
        "username": "test",
        "full_name": "테스터",
        "email": "test@maxdata.kr",
        "hashed_password": "$2b$12$16OwQZ31e2Ds/2ELoVCqgudzXZdG5VKd9AmNzMKq9dk2rZI.5rJRC",
        "disabled": False,
    },
}
