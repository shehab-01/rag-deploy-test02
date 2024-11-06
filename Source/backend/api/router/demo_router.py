import os
import json
import time
from pathlib import Path
from fastapi import Body, Depends, APIRouter, Request, HTTPException, status, Query, UploadFile, File, Form
from pydantic.types import Json

from api.utils.logger import logger
from api.utils.data_util import *
from api.model.models import ResData, User
from api.common.settings import settings
from api.common.token_helper import TokenHelper
from api.service import demo_service

from fastapi.responses import JSONResponse, Response
import psycopg2
from pydantic import BaseModel
import os


router = APIRouter(prefix="/api/demo")


@router.post("/timeout", response_model=ResData)
def demo_timeout(param: dict = Body()):
    print("demo.timeout")
    sec = 60 * 30
    # time.sleep(sec)
    print("End timeout.sleep:", sec)
    return ResData(data=dict(sec=sec), msg="")


@router.post("/test/conn", response_model=ResData)
def demo_test_conn(param: dict = Body()):
    print("demo.test.conn")
    for i in range(5):
        result = demo_service.demo_test_conn(None)
    return ResData(data=result, msg="")


@router.post("/test/view", response_model=ResData)
def demo_test_view(param: dict = Body()):
    print("demo.test.view.param:", param)
    result = demo_service.demo_test_view(param)
    return ResData(data=result, msg="")


@router.post("/pages/list", response_model=ResData)
def demo_pages_list(param: dict = Body()):
    print("demo.pages.list.param:", param)
    result = demo_service.demo_pages_list(param)
    return ResData(data=result, msg="")


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


@router.post("/test/db", response_model=ResData)
def demo_test_db(param: dict = Body()):
    result = demo_service.demo_test_db(None)
    return ResData(data=result, msg="")


@router.post("/get-directories", response_model=ResData)
def get_directories(param: dict = Body()):
    result = demo_service.getDirectories(None)
    return ResData(data=result, msg="")


@router.post("/get-file-content")
def get_file_content(param: dict = Body()):
    try:
        result = demo_service.getFileContent(param)
        if not result or "file_content" not in result:
            raise HTTPException(status_code=404, detail="File not found")

        pdf_content = result["file_content"]

        # If pdf_content is a memory address (large object)
        if isinstance(pdf_content, memoryview):
            # Convert memoryview to bytes
            pdf_bytes = pdf_content.tobytes()
        elif isinstance(pdf_content, bytes):
            pdf_bytes = pdf_content
        elif isinstance(pdf_content, str):
            # If it's base64 encoded
            import base64

            pdf_bytes = base64.b64decode(pdf_content)
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected file content format: {type(pdf_content)}")

        return Response(content=pdf_bytes, media_type="application/pdf")
    except psycopg2.Error as e:
        # Log the database error
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # Log the unexpected error
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
