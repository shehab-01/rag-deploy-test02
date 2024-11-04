from api.utils.logger import logger
from api.utils.data_util import *
from api.common.decorator import deco
from api.database.db_helper import db
from api.model.models import User


@deco.service
@deco.transaction(readonly=True)
def user_list(conn, param: dict):
    sql = f"""
        select row_number() over(order by a.user_nm) as rn
             , a.user_id
             , a.user_nm
             , a.user_div
             , a.user_type
             , a.birth_dt
             , a.sex
             , a.nation
             , a.email
             , a.telno
             , a.nrscr_no
             , a.use_yn
             , a.org_id
             , a.org_nm
             , to_char(a.reg_dtm, 'YYYY-MM-DD HH24:MI:SS') as reg_dtm
             , to_char(a.upd_dtm, 'YYYY-MM-DD HH24:MI:SS') as upd_dtm
          from user_info a
         where 1 = 1
         {"and a.user_id = %(user_id)s::varchar" if isNotBlank(param.get("user_id")) else ""}
         order by user_nm
    """
    rows = db.selectList(conn, sql, param)
    # logger.debug(f"rows: \n{rows}")
    return rows


@deco.service
@deco.transaction(readonly=True)
def user_view(conn, param: dict):
    sql = f"""
        select a.user_id
             , a.user_pw
             , a.user_nm
             , a.user_div
             , fn_cds_nm('CD001', a.user_div) as user_div_nm
             , a.user_type
             , fn_cds_nm('CD002', a.user_type) as user_type_nm
             , a.birth_dt
             , a.sex
             , a.nation
             , a.email
             , a.telno
             , a.nrscr_no
             , a.use_yn
             , a.org_id
             , null as org_nm
             , to_char(a.reg_dtm, 'YYYY-MM-DD HH24:MI:SS') as reg_dtm
             , to_char(a.upd_dtm, 'YYYY-MM-DD HH24:MI:SS') as upd_dtm
          from user_info a
         where 1 = 1
           and a.user_id = %(user_id)s::varchar
         limit 1
    """
    row = db.selectOne(conn, sql, param)
    # logger.debug(f"row: \n{row}")
    return row


@deco.service
@deco.transaction(readonly=True)
def user_check(conn, param):
    sql = f"""
        select 1
          from user_info
         where 1 = 1
           and user_id = %(user_id)s::varchar
         limit 1
    """
    row = db.selectOne(conn, sql, param)
    # logger.debug(f"row: \n{row}")
    return True if row is None else False


@deco.service
@deco.transaction()
def user_insert(conn, param: dict):

    # TEST: 임시..
    param.update(use_yn="Y")
    if isBlank(param.get("org_id")):
        param.update(org_id="maxted")

    sql = f"""
        insert into user_info (
            user_id, user_nm, user_div, user_type, user_pw, 
            birth_dt, sex, nation, email, telno, 
            nrscr_no, use_yn, org_id, reg_dtm, upd_dtm
        ) values (
            %(user_id)s, %(user_nm)s, %(user_div)s, %(user_type)s, %(user_pw)s, 
            %(birth_dt)s, %(sex)s, %(nation)s, %(email)s, %(telno)s, 
            %(nrscr_no)s, %(use_yn)s, %(org_id)s, now(), now()
        )
    """
    cnt = db.insert(conn, sql, param)
    return dict(cnt=cnt)


@deco.service
@deco.transaction()
def user_update(conn, param: dict):
    sql = f"""
        update user_info
           set upd_dtm = now()
           {", user_nm = %(user_nm)s" if isNotBlank(param.get("user_nm")) else ""}
           {", user_pw = %(user_pw)s" if isNotBlank(param.get("user_pw")) else ""}
           {", user_div = %(user_type)s" if isNotBlank(param.get("user_div")) else ""}
           {", user_type = %(user_type)s" if isNotBlank(param.get("user_type")) else ""}
           {", birth_dt = %(email)s" if isNotBlank(param.get("birth_dt")) else ""}
           {", sex = %(email)s" if isNotBlank(param.get("sex")) else ""}
           {", nation = %(email)s" if isNotBlank(param.get("nation")) else ""}
           {", nation = %(email)s" if isNotBlank(param.get("nation")) else ""}
           {", email = %(email)s" if isNotBlank(param.get("email")) else ""}
           {", telno = %(telno)s" if isNotBlank(param.get("telno")) else ""}
           {", nrscr_no = %(telno)s" if isNotBlank(param.get("nrscr_no")) else ""}
           {", use_yn = %(use_yn)s" if isNotBlank(param.get("use_yn")) else ""}
         where 1 = 1
           and user_id = %(user_id)s::varchar
    """
    cnt = db.update(conn, sql, param)
    # logger.debug(f"update.cnt: {cnt}")
    return dict(cnt=cnt)


@deco.service
@deco.transaction()
def user_delete(conn, param):
    sql = f"""
        delete from user_info
         where user_id = %(user_id)s::varchar
    """
    cnt = db.delete(conn, sql, param)
    # logger.debug(f"delete.cnt: {cnt}")
    return dict(cnt=cnt)


@deco.service
@deco.transaction()
def user_save(conn, param):
    sql = f"""
        insert into user_info as t (
            user_id, user_nm, user_pw, email, telno, use_yn, reg_dtm, upd_dtm
        ) values (
            %(user_id)s, %(user_nm)s, %(user_pw)s, %(email)s, %(telno)s, 'Y', now(), now()
        )
        on conflict (user_id)
        do update
        set user_nm = %(user_nm)s
          , user_pw = fn_nvl(%(user_pw)s, t.user_pw)
          , user_type = fn_nvl(%(user_type)s, t.user_type)
          , email = fn_nvl(%(email)s, t.email)
          , telno = fn_nvl(%(telno)s, t.telno)
          , use_yn = %(use_yn)s
          , upd_dtm = now()
    """
    cnt = db.save(conn, sql, param)
    return dict(cnt=cnt)


@deco.service
@deco.transaction()
def user_log(conn, param: dict):
    try:
        if param.get("user_id") and param.get("user_ip"):
            log = dict(log_type="W", user_id=param.get("user_id"), user_ip=param.get("user_ip"), user_cc=param.get("user_cc"), etc=param.get("etc"))
            sql = f"""
                insert into user_info_log (
                    log_type, log_dtm, user_id, user_ip, user_cc, etc
                ) values (
                    %(log_type)s, now(), %(user_id)s, %(user_ip)s, %(user_cc)s, %(etc)s
                )
            """
            db.insert(conn, sql, log)
            return True
    except Exception as e:
        logger.error(f"user_insert.error", e, exc_info=False)
        pass
    return False
