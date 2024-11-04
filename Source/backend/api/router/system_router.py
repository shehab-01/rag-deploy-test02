from fastapi import APIRouter, Request

from api.utils.logger import logger
from api.model.models import ResData
from api.service import system_service

router = APIRouter(prefix="/api/system")


@router.post("/check", response_model=ResData)
async def system_check(request: Request):
    param = await request.json()
    # print("request.param:", param)
    result = system_service.check(param)
    return ResData(data=result)
