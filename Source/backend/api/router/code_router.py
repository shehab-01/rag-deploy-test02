from fastapi import Body, Depends, APIRouter, Request

from api.utils.logger import logger
from api.model.models import ResData, User
from api.common.token_helper import TokenHelper
from api.service import code_service

router = APIRouter(prefix="/api/code")

"""
URL규칙
code/info
code/list
code/view
code/save
code/insert
code/update
code/delete
code/desc/list
code/desc/view
...
"""


@router.post("/info", response_model=ResData)
def code_info():
    param = dict(cd_id="")
    result = code_service.code_info(param)
    return ResData(data=result)


@router.post("/list", response_model=ResData)
def code_list(param: dict = Body()):
    result = code_service.code_list(param)
    return ResData(data=result)


@router.post("/save", response_model=ResData)
def code_save(param: dict = Body()):
    result = code_service.code_save(param)
    return ResData(data=result, msg="코드가 저장되었습니다.")


@router.post("/delete", response_model=ResData)
def code_delete(param: dict = Body()):
    result = code_service.code_delete(param)
    return ResData(data=result, msg="코드가 삭제되었습니다.")


@router.post("/desc/list", response_model=ResData)
def code_desc_list(param: dict = Body()):
    result = code_service.code_desc_list(param)
    return ResData(data=result)


@router.post("/desc/save", response_model=ResData)
def code_desc_save(param: dict = Body()):
    result = code_service.code_desc_save(param)
    return ResData(data=result, msg="상세코드가 저장되었습니다.")


@router.post("/desc/delete", response_model=ResData)
def code_desc_delete(param: dict = Body()):
    result = code_service.code_desc_delete(param)
    return ResData(data=result, msg="상세코드가 삭제되었습니다.")


@router.post("/desc/updateUseYn", response_model=ResData)
def code_desc_updateUseYn(param: dict = Body()):
    result = code_service.code_desc_updateUseYn(param)
    return ResData(data=result, msg=None)


# 업무코드
@router.post("/biz", response_model=ResData)
def code_biz(param: dict = Body()):
    result = code_service.code_biz(param)
    return ResData(data=result)
