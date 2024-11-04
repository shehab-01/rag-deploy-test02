from api.utils.logger import logger
from api.utils.data_util import *
from api.common.decorator import deco
from api.database.db_helper import db


# 코드정보(화면 진입시 캐싱할 코드 데이터)
@deco.service
@deco.transaction(readonly=True)
def code_info(conn, param):
    sql = f"""
        select row_number() over(order by cd_id, ord_seq) as rn
             , cd_id
             , cds_id
             , cds_nm
             , cds_text
          from code_desc
         where 1 = 1
           and use_yn = 'Y'
         order by cd_id, ord_seq
         --limit 1
    """
    rows = db.selectList(conn, sql, param)
    # raise Exception("오류테스트:code-info")

    logger.debug(f"rows: \n{rows}")
    return rows


# 코드목록
@deco.service
@deco.transaction(readonly=True)
def code_list(conn, param):
    sql = f"""
        select row_number() over(order by cd_id) as rn
             , cd_id
             , cd_nm
          from code_info
         where 1 = 1
           and use_yn = 'Y'
         {"and cd_id = %(cd_id)s" if isNotBlank(param.get("cd_id")) else ""}
         {"and cd_nm like concat('%%', %(cd_nm)s, '%%')" if isNotBlank(param.get("cd_nm")) else ""}
         order by cd_id
    """
    rows = db.selectList(conn, sql, param)
    return rows


# 코드 MaxId
def code_maxid(conn):
    sql = f"""
        select concat('CD', lpad((coalesce(max(substr(cd_id, 3))::int, 0) + 1)::varchar, 3, '0')) as max_id
        from code_info
        limit 1
    """
    row = db.selectOne(conn, sql, None)
    return row.get("max_id")


# 코드저장
@deco.service
@deco.transaction()
def code_save(conn, param):
    # 코드가 없으면 MaxId 채번
    if isBlank(param.get("cd_id")):
        max_id = code_maxid(conn)
        param.update(cd_id=max_id)
    param.update(cd_text="", use_yn="Y")

    sql = f"""
        insert into code_info as t
        (
            cd_id, cd_nm, cd_text, use_yn
        ) values (
            %(cd_id)s, %(cd_nm)s, %(cd_text)s, %(use_yn)s
        )
        on conflict (cd_id)
        do update
        set cd_nm = %(cd_nm)s
          , cd_text = fn_nvl(%(cd_text)s, t.cd_text)
    """
    cnt = db.save(conn, sql, param)
    logger.debug(f"save.cnt: {cnt}")
    return dict(cnt=cnt)


# 코드등록
@deco.service
@deco.transaction()
def code_insert(conn, param):
    max_id = code_maxid(conn)
    param.update(cd_id=max_id, cd_text=None, use_yn="Y")
    sql = f"""
        insert into code_info (
            cd_id, cd_nm, cd_text, use_yn
        ) values (
            %(cd_id)s, %(cd_nm)s, %(cd_text)s, %(use_yn)s
        )
    """
    cnt = db.insert(conn, sql, param)
    return dict(cnt=cnt)


# 코드수정
@deco.service
@deco.transaction()
def code_update(conn, param):
    sql = f"""
        update code_info
           set cd_nm = %(cd_nm)s
             , cd_text = %(cd_text)s
             , use_yn = %(use_yn)s
         where 1 = 1
           and cd_id = %(cd_id)s
           --and cd_id in ('CD001', 'CD002')
    """
    cnt = db.update(conn, sql, param)
    # cnt += db.update(conn, sql, dict(cd_text="TEST...1", cd_id="CD001"))
    # cnt += db.update(conn, sql, dict(cd_text="TEST...2", cd_id="CD002"))
    return dict(cnt=cnt)


# 코드삭제
@deco.service
@deco.transaction()
def code_delete(conn, param):
    sql = f"""
        delete from code_info
         where cd_id = %(cd_id)s
    """
    cnt = db.delete(conn, sql, param)
    return dict(cnt=cnt)


# 상세코드목록
@deco.service
@deco.transaction(readonly=True)
def code_desc_list(conn, param):
    sql = f"""
        select row_number() over(order by cd_id, ord_seq) as rn
             , cd_id
             , cds_id
             , cds_nm
             , cds_text
             , ord_seq
             , use_yn
          from code_desc
         where 1 = 1
         {"and cd_id = %(cd_id)s" if isNotBlank(param.get("cd_id")) else ""}
         order by cd_id, ord_seq
    """
    rows = db.selectList(conn, sql, param)
    return rows


# 상세코드저장
@deco.service
@deco.transaction()
def code_desc_save(conn, param):
    param.update(cds_grp=None, use_yn="Y")
    sql = f"""
        insert into code_desc as t
        (
            cd_id, cds_id, cds_nm, cds_text, cds_grp, ord_seq, use_yn
        ) values (
            %(cd_id)s, %(cds_id)s, %(cds_nm)s, %(cds_text)s, %(cds_grp)s, %(ord_seq)s, %(use_yn)s
        )
        on conflict (cd_id, cds_id)
        do update
        set cds_nm = %(cds_nm)s
          , cds_text = fn_nvl(%(cds_text)s, t.cds_text)
          , cds_grp = fn_nvl(%(cds_grp)s, t.cds_grp)
          , ord_seq = fn_nvl(%(ord_seq)s, t.ord_seq::varchar)::int
          , use_yn = %(use_yn)s
    """
    cnt = db.save(conn, sql, param)
    logger.debug(f"save.cnt: {cnt}")
    return dict(cnt=cnt)


# 상세코드삭제
@deco.service
@deco.transaction()
def code_desc_delete(conn, param):
    sql = f"""
        delete from code_desc
         where cds_id = %(cds_id)s
    """
    cnt = db.delete(conn, sql, param)
    return dict(cnt=cnt)


# 상세코드 사용여부 업데이트
@deco.service
@deco.transaction()
def code_desc_updateUseYn(conn, param):
    sql = f"""
        update code_desc
           set use_yn = %(use_yn)s
         where 1 = 1
           and cd_id = %(cd_id)s
           and cds_id = %(cds_id)s
    """
    cnt = db.update(conn, sql, param)
    return dict(cnt=cnt)


# 업무코드
@deco.service
@deco.transaction(readonly=True)
def code_biz(conn, param):
    sql = None
    rows = None
    code_biz = param.get("code_biz")

    # 그룹 코드목록
    if code_biz == "group":
        sql = f"""
        """

    # 사용자 코드목록
    elif code_biz == "users":
        sql = f"""
            select a.user_id as key
                 , a.user_nm as val
              from tb_user a
                 , tb_group b
             where 1 = 1
               and a.grp_id = b.grp_id
               and b.ten_id = 'maxted'
               and a.use_yn = 'Y'
               and a.user_type in ('M', 'A')
             order by a.user_nm
        """

    if sql is not None:
        rows = db.selectList(conn, sql, param)
    return rows
