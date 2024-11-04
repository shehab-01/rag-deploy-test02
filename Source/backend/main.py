import os
import asyncio
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse
from starlette.staticfiles import StaticFiles
from api.database.db_helper import db_helper

from api.utils.logger import logger
from api.common import exceptions as ex
from api.common.settings import settings
from api.common.api_middleware import ApiHTTPMiddleware

# import router
from api.router import system_router
from api.router import main_router
from api.router import code_router
from api.router import user_router
from api.router import demo_router
from api.router import ai_url_router
from api.router import chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await server_startup()
    yield
    await server_shutdown()


app = FastAPI(
    title="FastAPI",
    description="FastAPI",
    version="0.0.0",
    terms_of_service="",
    contact={
        # "name": "맥스테드",
        # "url": "https://maxted.kr",
        # "email": "info@maxted.kr",
    },
    license_info={
        # "name": "Apache 2.0",
        # "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)  # fmt: skip

# CORS
origins = [
    "*",
    "http://localhost", 
    "http://localhost:8000", 
    "http://localhost:9000", 
]  # fmt: skip
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # fmt: skip
# app.add_middleware(ApiHTTPMiddleware)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONT_DIR = os.path.join(BASE_DIR, "rndops-fe")

app.include_router(system_router.router, tags=["system"])
app.include_router(main_router.router, tags=["main"])
app.include_router(code_router.router, tags=["code"])
app.include_router(user_router.router, tags=["user"])
app.include_router(demo_router.router, tags=["demo"])
app.include_router(ai_url_router.router, tags=["ai"])
app.include_router(chat_router.router, tags=["chat"])
# app.mount("/image", StaticFiles(directory=FRONT_DIR + "/dist/image"))
# app.mount("/assets", StaticFiles(directory=FRONT_DIR + "/dist/assets"))
# app.mount("/plugins", StaticFiles(directory=FRONT_DIR + "/dist/plugins"))

# DATA 경로추가
app.mount("/nas", StaticFiles(directory=os.getenv("PATH_NAS_ROOT")))
app.mount("/test", StaticFiles(directory=os.getenv("PATH_TEST_ROOT")))

# TEST: 환경변수 추가수정..
if settings.APP_ENV == "local":
    pass


# Index
# @app.get("/")
# def index():
#     return FileResponse(FRONT_DIR + "/dist/index.html")


# @app.get("/favicon.png", include_in_schema=False)
# def favicon():
#     return FileResponse(FRONT_DIR + "/dist/favicon.png")


# Health check
@app.get("/health")
def health_check():
    # return JSONResponse(
    #     status_code=status.HTTP_200_OK,
    #     content={"detail": "OK"}
    # )  # fmt: skip
    return PlainTextResponse("OK", status_code=status.HTTP_200_OK)


# Exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print("main.exception_handler:", type(exc))
    return await ex.json_responser(exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print("main.http_exception_handler:", type(exc))
    return await ex.json_responser(exc)


@app.exception_handler(404)
async def http_404_handler(request: Request, exc: RequestValidationError):
    # path = request.url.path
    # if path.startswith("/public"):
    #     return FileResponse(FRONT_DIR + "/public")
    # else:
    #     return FileResponse(FRONT_DIR + "/dist/index.html")

    return RedirectResponse("/")


# 서버시작 이벤트
# @app.on_event("startup")
async def server_startup():
    logger.info("Server started..")
    # print("settings:", os.getenv("APP_ENV"))
    # print("settings:", os.environ["APP_ENV"])
    db_helper.initialize_connection_pool()


# 서버종료 이벤트
# Press CTRL+C to quit, Bug:reload/worker 옵션시 호출안됨
# @app.on_event("shutdown")
async def server_shutdown():
    logger.info("Server Shutdown..")
    db_helper.shutdown_connection_pool()


# if __name__ == "__main__":
#     print("fastapi.main")
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True, workers=3, log_config="log.yaml")
