# routers/chat_router.py
from fastapi import APIRouter, Body, status
from typing import Optional
from pydantic import BaseModel
from api.model.models import ResData
from api.service import chat_service

router = APIRouter(prefix="/api/chat")


class SessionCreate(BaseModel):
    title: str
    user_email: str
    prompt_id: int
    prompt_name: str


class MessageCreate(BaseModel):
    session_id: str
    type: str
    content: str
    source: Optional[str] = ""


@router.post("/sessions", response_model=ResData)
async def create_session(param: SessionCreate):
    print("Session router", param.model_dump())
    try:
        result = chat_service.create_session(param.model_dump())
        return ResData(status=status.HTTP_200_OK, msg="Session created successfully", data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/messages", response_model=ResData)
async def save_message(param: MessageCreate):
    print("Message Router")
    try:
        result = chat_service.save_message(param.model_dump())
        return ResData(status=status.HTTP_200_OK, msg="Message saved successfully", data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/list", response_model=ResData)
async def get_chat_list(param: dict = Body()):
    print("List router")
    try:
        result = chat_service.get_chat_list(param)
        return ResData(status=status.HTTP_200_OK, data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/messages/list", response_model=ResData)
async def get_chat_messages(param: dict = Body()):
    print("Message List router")
    try:
        result = chat_service.get_chat_messages(param)
        return ResData(status=status.HTTP_200_OK, data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/session-list", response_model=ResData)
async def get_chat_session_list():
    print("side list")
    try:
        result = chat_service.get_chat_session_list()
        return ResData(status=status.HTTP_200_OK, data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/full-chat-list", response_model=ResData)
async def get_chat_full_chat_list(param: dict = Body()):
    print("full chat list", param)
    try:
        result = chat_service.get_chat_full_chat_list(param)
        return ResData(status=status.HTTP_200_OK, data=result)
    except Exception as e:
        return ResData(status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=str(e), data=None)


@router.post("/prompt_list", response_model=ResData)
def get_prompt_list():
    # param = dict(cd_id="")
    result = chat_service.get_prompt_list()
    return ResData(data=result)


@router.post("/prompt_detl", response_model=ResData)
def get_prompt_list_detl(param: dict = Body()):
    # param = dict(cd_id="")
    print(param)
    prompt_id = param["prompt_id"]
    result = chat_service.get_prompt_list_detl(param)
    return ResData(data=result)


@router.post("/session-delete", response_model=ResData)
def delete_session(param: dict = Body()):
    # param = dict(cd_id="")
    print(param)
    # prompt_id = param["prompt_id"]
    chat_service.delete_session_msgs(param)
    result = chat_service.delete_session(param)
    return ResData(data=result, msg="셰선 삭제 완료")


@router.post("/prompt-save", response_model=ResData)
def create_new_prompt(param: dict = Body()):
    # param = dict(cd_id="")
    print(param)
    # prompt_id = param["prompt_id"]
    result = chat_service.create_new_prompt(param)
    return ResData(data=result, msg="")
