import os
import json
import time
from pathlib import Path
from fastapi import Body, Depends, APIRouter, Request, HTTPException, status, Query
from pydantic.types import Json

from api.utils.logger import logger
from api.utils.data_util import *
from api.model.models import ResData, User
from api.common.settings import settings
from api.common.token_helper import TokenHelper
from api.service import demo_service
from api.rag import test
from api.rag import query_processing
from api.rag import utils

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import os
import logging


router = APIRouter(prefix="/api/ai")


# @router.post("/ask-ai-assistant", response_model=ResData)
# async def ask_ai(param: dict = Body()):
#     question = param["question"]
#     directory_name = param["directory_name"]
#     question_language = param["question_lang"]
#     print(param)
#     # return "rets"
#     resultvd = await query_processing.process_query(question, directory_name, question_language)
#     result = "fsdf"
#     return ResData(data=resultvd, msg="")
#     return JSONResponse(content=utils.convert_to_json_serializable(result))


@router.post("/ask-ai-assistant")
async def ask_ai(param: dict = Body()):
    question = param["question"]
    directory_name = param["directory_name"]
    question_language = param["question_lang"]
    print(param)

    resultvd = await query_processing.process_query(question, directory_name, question_language)
    result = "fsdf"  # This line seems unnecessary, you might want to use resultvd instead
    content = utils.convert_to_json_serializable(resultvd)
    return JSONResponse(content)
