from string_utils import *
from api.utils.logger import logger
from api.common.decorator import deco
from api.database.db_helper import db


# TEST:
@deco.service
@deco.transaction(readonly=True)
def check(conn, param):
    sql = f"""
        show search_path
    """
    row = db.selectList(conn, sql, None)

    sql = f"""
        select *
          from code_info
    """
    rows = db.selectList(conn, sql, None)
    result = dict(path=row, test=rows)
    return result
