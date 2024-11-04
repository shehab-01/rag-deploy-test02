import os
import json
import time
from pathlib import Path
from fastapi import Body, Depends, APIRouter, Request, HTTPException, status, Query, UploadFile, File, Form
from pydantic.types import Json
from fastapi.responses import StreamingResponse


from api.utils.logger import logger
from api.utils.data_util import *
from api.model.models import ResData, User
from api.common.settings import settings
from api.common.token_helper import TokenHelper


from api.rag_url.chat import search

from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os


router = APIRouter(prefix="/api/ai-url")


async def generate_chunks(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"


@router.post("/ask")
async def ask_ai(param: dict = Body()):

    question = param["question"]
    print(param)

    response = await search.search_query_ai(question)

    # for chunk in response:
    #     if chunk.choices[0].delta.content is not None:
    #         print(chunk.choices[0].delta.content, end="", flush=True)

    return StreamingResponse(
        generate_chunks(response),
        media_type="text/event-stream",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Important for Nginx
        },
    )
