import os
import json
import time
import shutil
import datetime

from string_utils import *
from api.utils.logger import logger
from api.utils.data_util import *
from api.common.decorator import deco
from api.database.db_helper import db_helper, db


@deco.service
@deco.transaction(readonly=True)
def demo_test_conn(conn, param):
    sql = f"""
        select 1
    """
    rows = db.selectList(conn, sql, param)
    return rows


@deco.service
@deco.transaction(readonly=True)
def demo_test_view(conn, param):
    sql = f"""
        select 1
         where 1 = 2
         limit 1
    """
    row = db.selectOne(conn, sql, param)
    print("row:", row)
    return row


@deco.service
def demo_test_list(param):
    # 조건 동적쿼리 멀티라인 테스트..
    sql = f"""
        select *
          from tb_code
         where 1 = 1
         {"and cd_id = %(cd_id)s" 
          " or cd_id = 'CD999'"
          if is_full_string(param.get("cd_id")) else ""}
         order by cd_id
         --limit 1
    """
    with db_helper.get_conn() as (conn, cursor):
        rows = db.selectList(conn, sql, param)
        # raise Exception("오류테스트:code-list-db")

    if True:
        print("Exception test...")
        # i = 3/0
        # raise Exception("오류테스트:code-list")

    print("rows:", rows)
    return rows


@deco.service
@deco.transaction(readonly=True)
def demo_pages_list(conn, param):
    sql = f"""
        with vt as (
            select no
            from generate_series(1, 100000) no
        )
        select no
             , concat('Name-', lpad(no::varchar, 6, '0')) as name
             , floor(((no + 1 / 7) * 333) %% 100) as c1
             , floor(((no + 1 / 3) * 555) %% 100) as c2
             , floor(((no + 1 / 3) * 555) %% 100) as c3
             , trunc(random()*10 + 1) c4
             , trunc(random()*10 + 1) c5
             , trunc(random()*10 + 1) c6
          from vt
         where 1 = 1
    """
    # rows = db.selectList(conn, sql, param)
    rows = db.selectPaging(conn, sql, param)
    return rows


"""
데모: 데이터 업데이트..
"""


@deco.service
def demo_insert(param):
    return None


@deco.service
def demo_update(param):
    # print("service.conn:", conn)
    print("service.param:", param)
    sql = f"""
        update tb_code
           set cd_text = %(cd_text)s
         where 1 = 1
           and cd_id = %(cd_id)s
           --and cd_id in ('CD001', 'CD002')
    """
    with db_helper.get_conn() as (conn, cursor):
        cnt = 0
        cnt = db.update(conn, sql, param)
        # cnt += db.update(conn, sql, dict(cd_text="TEST...1", cd_id="CD001"))
        # cnt += db.update(conn, sql, dict(cd_text="TEST...2", cd_id="CD002"))
        print("update.cnt:", cnt)

        if True:
            print("Exception test...")
            # raise Exception("오류테스트:code-update")

    print("code-update end..")
    return dict(cnt=cnt)


@deco.service
def demo_delete(param):
    return None


# Ai


@deco.service
@deco.transaction(readonly=True)
def demo_test_db(conn, param):
    sql = f"""
        select * FROM tb_test

    """
    row = db.selectList(conn, sql, param)
    print("row:", row)
    return row


@deco.service
@deco.transaction(readonly=True)
def getFileContent(conn, param):
    sql = """
        SELECT 
            file_content 
        FROM tb_rag 
        WHERE file_name = %(filename)s
    """
    row = db.selectOne(conn, sql, param)
    if row and "file_content" in row:
        # If it's a large object, read it
        if isinstance(row["file_content"], memoryview):
            return {"file_content": row["file_content"].tobytes()}
        return row
    return None


@deco.service
@deco.transaction(readonly=True)
def getDirectories(conn, param):
    sql = f"""
        select 
            file_name
            , directory_path
            , id 
        from tb_rag

    """
    rows = db.selectList(conn, sql, param)
    print("row:", rows)
    return rows
