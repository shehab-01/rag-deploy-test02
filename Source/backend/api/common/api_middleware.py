import re
import time

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from api.common import config, consts
from api.common import exceptions as ex
from api.common.token_helper import Token, TokenHelper
from api.model.models import User
from api.utils.logger import logger, api_logger


class ApiHTTPMiddleware(BaseHTTPMiddleware):
    async def set_empty_body(self, request: Request):
        receive_ = await request._receive()
        if len(receive_["body"]) == 0:
            receive_["body"] = b"{}"

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print("ApiHTTPMiddleware.dispatch")

        # request.body
        # await self.set_empty_body(request)
        # body = await request.body()
        # print("ApiHTTPMiddleware.body:", body)

        # request.state.req_time = D.datetime()
        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.service = None

        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        headers = request.headers
        cookies = request.cookies

        url = request.url.path

        if await url_pattern_check(url, consts.EXCEPT_PATH_REGEX) or url in consts.EXCEPT_PATH_LIST:
            response = await call_next(request)
            if url != "/":
                await api_logger(request=request, response=response)
            return response

        try:
            # TEST: skip
            # response = await call_next(request)
            # return response

            # print("headers.key:", headers.keys())
            # api 인경우 헤더로 토큰 검사
            if url.startswith("/api"):
                if url.startswith("/api/services"):
                    if not config.conf().DEBUG:
                        try:
                            qs = str(request.query_params)
                            qs_list = qs.split("&")
                            qs_dict = {qs_split.split("=")[0]: qs_split.split("=")[1] for qs_split in qs_list}
                        except Exception:
                            raise ex.APIQueryStringEx()

                        qs_keys = qs_dict.keys()
                        # user_info = to_dict(api_key.users)
                        # request.state.user = UserToken(**user_info)

                    else:
                        # 토큰유저
                        if "authorization" in headers.keys():
                            access_token = headers.get("Authorization").replace("Bearer ", "")
                            current_user: User = await TokenHelper.get_curr_user(access_token)
                            user: User = await TokenHelper.user(current_user)
                            request.state.user = user
                        # 토큰없음
                        else:
                            raise ex.NotAuthorized()

                    response = await call_next(request)
                    return response

                else:
                    # 토큰유저
                    if "authorization" in headers.keys():
                        access_token = headers.get("Authorization").replace("Bearer ", "")
                        current_user: User = await TokenHelper.get_curr_user(access_token)
                        user: User = await TokenHelper.user(current_user)
                        request.state.user = user
                    # 토큰없음
                    else:
                        raise ex.NotAuthorized()

            # api가 아닌 경우 쿠키에서 토큰 검사
            else:
                # TEST:
                cookies["Authorization"] = (
                    "Bearer XXXXX"
                )  # fmt: skip
                if "Authorization" not in cookies.keys():
                    raise ex.NotAuthorized()

                access_token = cookies.get("Authorization").replace("Bearer ", "")
                current_user: User = await TokenHelper.get_curr_user(access_token)
                user: User = await TokenHelper.user(current_user)
                request.state.user = user

            response = await call_next(request)
            # await api_logger(request=request, response=response)

        except Exception as e:
            response = await ex.json_responser(e)
            logger.error(e, exc_info=False)

        return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False
