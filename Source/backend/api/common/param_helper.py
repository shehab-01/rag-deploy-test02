import json
from typing import Union
from fastapi import Depends, Request, HTTPException, status

from api.utils.logger import logger
from api.common import config, consts
from api.common import exceptions as ex


class ParamHelper:
    def __init__(self):
        pass

    async def query_dict(request: Request) -> dict:
        return dict(request.query_params)
