# import httpx

from typing import Union
from typing import Optional
from typing_extensions import Annotated
from fastapi import Header, Body, Depends, APIRouter, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from api.utils.logger import logger
from api.model.models import ResData, User
from api.common.token_helper import Token, TokenHelper
from api.common.settings import settings
from api.common import config, consts
from api.service import user_service


router = APIRouter(prefix="/api/user")


"""
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"}
        )  # fmt: skip
    # make access token
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )  # fmt: skip
    return {"token_type": "Bearer", "access_token": access_token}
"""


# 로그인
@router.post("/login", response_model=Token)
def user_login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"api.user.login.. {form_data.username}")
    # check user and password
    user_data = TokenHelper.authenticate_user(form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )  # fmt: skip

    # make access token
    access_token = TokenHelper.create_access_token(
        data={"sub": user_data.user_id},
        expires_delta=timedelta(minutes=consts.JWT_EXPIRE_MINUTES)
    )  # fmt: skip

    # user log
    if settings.APP_ENV != "local":
        headers = request.headers
        user_service.user_log(dict(
            user_id = user_data.user_id,
            user_ip = headers.get('x-real-ip'),
            user_cc = headers.get('x-real-cc'),
            etc = headers.get('user-agent'),
        ))  # fmt: skip

    return {"token_type": "Bearer", "access_token": access_token}


# 로그아웃
@router.get("/logout", response_model=ResData)
def user_logout(request: Request, user: User = Depends(TokenHelper.user)):
    logger.info(f"api.user.logout.. {user.user_id}")
    return ResData()


# 사용자 중복체크
@router.post("/check", response_model=ResData)
def user_check(param: dict = Body()):
    # param = await request.json()
    valid = user_service.user_check(param)
    return ResData(data=dict(valid=valid))


# 사용자가입
@router.post("/join", response_model=ResData)
def user_join(param: dict = Body()):
    # param = await request.json()
    hashed_password = TokenHelper.get_password_hash(param.get("user_pw"))
    param.update(user_pw=hashed_password)
    user_service.user_insert(param)
    return ResData(msg="사용자로 등록되었습니다.")


# 현재세션 사용자정보
@router.get("/info", response_model=ResData)
def user_info(request: Request, user: User = Depends(TokenHelper.user)):
    return ResData(data=dict(user=user))


# 현재세션 사용자수정
@router.post("/update", response_model=ResData)
def user_update(param: dict = Body(), user: User = Depends(TokenHelper.user)):
    if param.get("user_pw") is not None and param.get("user_pw") == param.get("user_pw2"):
        hashed_password = TokenHelper.get_password_hash(param.get("user_pw"))
        param.update(user_pw=hashed_password)

    # 사용자 등록
    user_service.user_update(param)

    # 사용자 재조회
    user_data = user_service.user_view(param)
    user: User = User(**user_data)

    # 비밀번호가 있으면 제거하고 리턴
    # user.pop("user_pw", None)
    # user.pop("user_pw2", None)
    return ResData(data=dict(user=user))


# 조회 사용자목록
@router.post("/list", response_model=ResData)
def user_list(param: dict = Body(), user: User = Depends(TokenHelper.user)):
    user_list = user_service.user_list(param)
    return ResData(data=user_list)


# 조회 사용자정보
@router.post("/view", response_model=ResData)
def user_view(param: dict = Body(), user: User = Depends(TokenHelper.user)):
    user_view = user_service.user_view(param)
    user: User = User(**user_view)
    return ResData(data=user)


# 조회 사용자저장
@router.post("/save", response_model=ResData)
def user_save(param: dict = Body(), user: User = Depends(TokenHelper.user)):
    if param.get("user_pw") is not None and param.get("user_pw") == param.get("user_pw2"):
        hashed_password = TokenHelper.get_password_hash(param.get("user_pw"))
        param.update(user_pw=hashed_password)

    # 사용자정보 저장
    user_service.user_save(param)

    # 사용자정보 재조회
    user_view = user_service.user_view(param)
    user: User = User(**user_view)

    return ResData(data=dict(user=user), msg="사용자정보가 저장되었습니다.")


# 조회 사용자삭제
@router.post("/delete", response_model=ResData)
def user_delete(param: dict = Body(), user: User = Depends(TokenHelper.user)):
    result = user_service.user_delete(param)
    return ResData(data=result, msg="사용자정보가 삭제되었습니다.")


# TEST:
# 사용자 request
@router.post("/request", response_model=ResData)
def user_request(request: Request):
    headers = request.headers
    client = request.client
    print("request.headers:", headers)
    print("user-agent:", headers.get("user-agent"))

    """"""
    ip_info = {}
    # res = httpx.get("http://ipinfo.io")
    # res = httpx.get("http://ip-api.com/json/1.222.84.186")
    # res = httpx.get("https://freeipapi.com/api/json/1.222.84.186")
    # res = httpx.get("https://ip2c.org/?ip=1.222.84.186")
    # res = httpx.get("http://ip2c.org/?ip=1.222.84.186")
    # if res.status_code == status.HTTP_200_OK:
    #     ip_info = res.json()

    """"""
    # async with httpx.AsyncClient() as async_client:
    #     res = await async_client.get("https://ip2c.org/?ip=1.222.84.186")
    #     if res.status_code == 200:
    #         print("httpx.res:", res.text)

    return ResData(data=dict(headers=headers, client=client))
