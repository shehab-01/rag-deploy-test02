import json
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extensions import connection, cursor

from api.utils.logger import logger
from api.common import exceptions as ex
from api.database.db_helper import db_helper, db


class Deco:
    def test(self, func):
        def wrapper(*args, **kwargs):
            # print(func.__name__, '함수시작')
            result = func(*args, **kwargs)
            # print(func.__name__, '함수종료')
            return result

        return wrapper

    def service(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    def transaction(self, readonly=None):
        def wrapper_func(func):
            def wrapper(*args, **kwargs):
                try:
                    connection_pool: ThreadedConnectionPool = db_helper.get_connection_pool()
                    conn: connection = connection_pool.getconn()

                    # TEST: 스키마변경
                    # cursor = conn.cursor()
                    # cursor.execute("SET search_path TO maxted")
                    # conn.commit()

                    conn.readonly = readonly
                    if conn.readonly == None:
                        conn.autocommit = False
                    else:
                        conn.autocommit = conn.readonly

                    # TODO: connection 참여처리..
                    # if args is not None and type(args[0]) is connection:
                    #     result = func(*args, **kwargs)
                    # else:
                    #     result = func(conn, *args, **kwargs)

                    result = func(conn, *args, **kwargs)

                    if conn.autocommit is False:
                        conn.commit()
                except Exception as e:
                    if conn.autocommit is False:
                        conn.rollback()
                    raise ex.RuntimeEx(e)
                finally:
                    connection_pool.putconn(conn)  # 연결반환
                return result

            return wrapper

        return wrapper_func


deco = Deco()
