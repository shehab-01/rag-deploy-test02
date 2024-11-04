# auth
# openssl rand -hex 32
# JWT_SECRET = "ABCD1234!"
JWT_SECRET = "866b054834a6533c32b7abe479b1a6cb6a1d7b2af0c3cb4802b9c1fff622430f"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 1440 * 7
MAX_API_KEY = 3
MAX_API_WHITELIST = 10
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
EXCEPT_PATH_LIST = [
    "/",
    "/health",
    "/api/user/login",
    "/openapi.json"
]  # fmt: skip
