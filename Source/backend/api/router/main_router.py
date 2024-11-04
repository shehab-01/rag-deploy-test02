from fastapi import Body, Depends, APIRouter, Request

from api.utils.logger import logger
from api.model.models import ResData, User
from api.common.token_helper import TokenHelper
from api.service import main_service
import re

router = APIRouter(prefix="/api/main")


@router.get("")
def test(request: Request):
    return {"main": "OK"}
