import psycopg2
from fastapi import HTTPException, status
from starlette.responses import JSONResponse

from api.model.models import Error, ErrData
from api.common.consts import MAX_API_KEY, MAX_API_WHITELIST


class StatusCode:
    HTTP_400 = status.HTTP_400_BAD_REQUEST
    HTTP_401 = status.HTTP_401_UNAUTHORIZED
    HTTP_403 = status.HTTP_403_FORBIDDEN
    HTTP_404 = status.HTTP_404_NOT_FOUND
    HTTP_405 = status.HTTP_405_METHOD_NOT_ALLOWED
    HTTP_500 = status.HTTP_500_INTERNAL_SERVER_ERROR


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(self, *, status_code: int = StatusCode.HTTP_500, code: str = None, msg: str = None, detail: str = None, ex: Exception = None):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"로그인이 필요한 서비스 입니다.",
            detail="Authorization Required",
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            code=f"{StatusCode.HTTP_401}{'2'.zfill(4)}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"{StatusCode.HTTP_401}{'3'.zfill(4)}",
            ex=ex,
        )


class TokenCredentialEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"자격증명을 확인할 수 없습니다.",
            detail="Could not validate credentials.",
            code=f"{StatusCode.HTTP_401}{'4'.zfill(4)}",
            ex=ex,
        )


class NotFoundUserEx(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"해당 유저를 찾을 수 없습니다.",
            detail=f"Not Found User ID : {user_id}",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class MaxKeyCountEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"API 키 생성은 {MAX_API_KEY}개 까지 가능합니다.",
            detail="Max Key Count Reached",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )


class MaxWLCountEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"화이트리스트 생성은 {MAX_API_WHITELIST}개 까지 가능합니다.",
            detail="Max Whitelist Count Reached",
            code=f"{StatusCode.HTTP_400}{'3'.zfill(4)}",
            ex=ex,
        )


class InvalidIpEx(APIException):
    def __init__(self, ip: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"{ip}는 올바른 IP 가 아닙니다.",
            detail=f"invalid IP : {ip}",
            code=f"{StatusCode.HTTP_400}{'4'.zfill(4)}",
            ex=ex,
        )


class APIQueryStringEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"쿼리스트링은 key, timestamp 2개만 허용되며, 2개 모두 요청시 제출되어야 합니다.",
            detail="Query String Only Accept key and timestamp.",
            code=f"{StatusCode.HTTP_400}{'5'.zfill(4)}",
            ex=ex,
        )


class APIHeaderInvalidEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"헤더에 키 해싱된 Secret 이 없거나, 유효하지 않습니다.",
            detail="Invalid HMAC secret in Header",
            code=f"{StatusCode.HTTP_400}{'6'.zfill(4)}",
            ex=ex,
        )


class APITimestampEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"쿼리스트링에 포함된 타임스탬프는 KST 이며, 현재 시간보다 작아야 하고, 현재시간 - 10초 보다는 커야 합니다.",
            detail="timestamp in Query String must be KST, Timestamp must be less than now, and greater than now - 10.",
            code=f"{StatusCode.HTTP_400}{'7'.zfill(4)}",
            ex=ex,
        )


class KakaoSendFailureEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"카카오톡 전송에 실패했습니다.",
            detail=f"Failed to send KAKAO MSG.",
            code=f"{StatusCode.HTTP_400}{'8'.zfill(4)}",
            ex=ex,
        )


class NoKeyMatchEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"해당 키에 대한 권한이 없거나 해당 키가 없습니다.",
            detail="No Keys Matched",
            code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
            ex=ex,
        )


class NotFoundAccessKeyEx(APIException):
    def __init__(self, api_key: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"API 키를 찾을 수 없습니다.",
            detail=f"Not found such API Access Key : {api_key}",
            code=f"{StatusCode.HTTP_404}{'2'.zfill(4)}",
            ex=ex,
        )


class RuntimeEx(APIException):
    def __init__(self, ex: Exception = None):
        print(type(ex))
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"[Runtime] 내부 서버 오류입니다.",
            detail=str(ex),
            code=f"{StatusCode.HTTP_500}{'1'.zfill(4)}",
            ex=ex,
        )  # fmt: skip


class DBFailureEx(APIException):
    # def __init__(self, ex: Exception = None):
    #     super().__init__(
    #         status_code=StatusCode.HTTP_500,
    #         msg=f"[DB] 내부 서버 오류입니다.",
    #         detail="Internal Server Error",
    #         code=f"{StatusCode.HTTP_500}{'2'.zfill(4)}",
    #         ex=ex,
    #     )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SqlFailureEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"[SQL] 내부 서버 오류입니다.",
            detail="Internal Server Error",
            code=f"{StatusCode.HTTP_500}{'3'.zfill(4)}",
            ex=ex,
        )


async def exception_handler(error: Exception):
    if isinstance(error, psycopg2.Error):
        error = SqlFailureEx(ex=error)
    elif isinstance(error, HTTPException):
        error = APIException(ex=error, detail=str(error.detail), status_code=int(error.status_code))
    elif not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error


async def json_responser(error: Exception):
    error = await exception_handler(error)
    error_data = ErrData(
        status=error.status_code,
        msg=error.msg,
        error=Error(
            code=error.code,
            type=error.ex.__class__.__name__,
            detail=error.detail
        )
    )  # fmt: skip
    response = JSONResponse(status_code=error.status_code, content=error_data.model_dump())
    response.headers["Access-Control-Allow-Origin"] = "*"
    print("exceptions.json_responser:", response.body)
    return response
