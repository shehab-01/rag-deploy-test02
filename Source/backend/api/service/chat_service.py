# services/chat_service.py
from api.utils.logger import logger
from api.utils.data_util import *
from api.common.decorator import deco
from api.database.db_helper import db


@deco.service
@deco.transaction(readonly=False)
def create_session(conn, param):
    print("From service: ")
    sql = """
        INSERT INTO tb_rag_chat_sessions 
        (title, user_email, prompt_id, prompt_name)
        VALUES 
        (%(title)s, %(user_email)s, %(prompt_id)s, %(prompt_name)s)
        RETURNING id, title, prompt_name, created_at
    """
    try:
        result = db.selectOne(conn, sql, param)
        return result
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=False)
def save_message(conn, param):
    sql = """
        INSERT INTO tb_rag_chat_messages 
        (session_id, type, content, source)
        VALUES 
        (%(session_id)s, %(type)s, %(content)s, %(source)s)
        RETURNING id, type, content, created_at
    """
    try:
        result = db.selectOne(conn, sql, param)
        return result
    except Exception as e:
        logger.error(f"Error saving message: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=True)
def get_chat_list(conn, param):
    sql = """
        SELECT 
            cs.id,
            cs.title,
            cs.prompt_name,
            cs.created_at,
            COUNT(cm.id) as message_count
        FROM tb_rag_chat_sessions cs
        LEFT JOIN tb_rag_chat_messages cm ON cs.id = cm.session_id
        WHERE cs.user_email = %(user_email)s
        GROUP BY cs.id, cs.title, cs.prompt_name, cs.created_at
        ORDER BY cs.created_at DESC
    """
    try:
        rows = db.selectList(conn, sql, param)
        logger.debug(f"chat_list rows: \n{rows}")
        return rows
    except Exception as e:
        logger.error(f"Error getting chat list: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=True)
def get_chat_messages(conn, param):
    sql = """
        SELECT 
            id,
            type,
            content,
            source,
            created_at
        FROM tb_rag_chat_messages 
        WHERE session_id = %(session_id)s
        ORDER BY created_at
    """
    try:
        rows = db.selectList(conn, sql, param)
        logger.debug(f"tb_rag_chat_messages rows: \n{rows}")
        return rows
    except Exception as e:
        logger.error(f"Error getting chat messages: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=True)
def get_chat_session_list(conn):
    sql = """
        SELECT 
            title 
            , id
            , prompt_name 
            , prompt_id 
            , created_at 	

        FROM tb_rag_chat_sessions
        ORDER BY created_at DESC
    """
    try:
        rows = db.selectList(conn, sql)
        logger.debug(f"tb_rag_chat_side_list rows: \n{rows}")
        return rows
    except Exception as e:
        logger.error(f"Error getting chat messages: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=True)
def get_chat_full_chat_list(conn, param):
    try:
        # Base SQL query
        base_sql = """
            SELECT 
                content,
                type
            FROM tb_rag_chat_messages
            WHERE 1 = 1
        """

        # Add session_id condition if present
        if isNotBlank(param.get("session_id")):
            base_sql += " AND session_id = %(session_id)s"

        # Add order by
        base_sql += " ORDER BY created_at"

        # Execute query with parameters
        rows = db.selectList(conn, base_sql, param)
        logger.debug(f"tb_rag_chat_messages rows: \n{rows}")
        return rows

    except Exception as e:
        logger.error(f"Error getting chat messages: {str(e)}")
        raise e


@deco.service
@deco.transaction(readonly=True)
def get_prompt_list(conn):
    sql = f"""
        select
            prompt_id,
            prompt_name,
            description
        from tb_rag_prompt_collection
         where 1 = 1

    """
    rows = db.selectList(conn, sql)
    # print("rows:", rows)
    return rows


@deco.service
@deco.transaction(readonly=True)
def get_prompt_list_detl(conn, param):
    sql = f"""
        select 
            prompt_id, 
            prompt_name,
            description,
            prompt_type,
            max_output_token,
            temperature,
            topP,
            prompt_content
        from tb_rag_prompt_collection
         where 1 = 1  
        {"and prompt_id = %(prompt_id)s" if isNotBlank(param.get("prompt_id")) else ""}
    """
    row = db.selectOne(conn, sql, param)
    # print("rows:", rows)
    return row


# Delete session msgs
@deco.service
@deco.transaction()
def delete_session_msgs(conn, param):
    sql = f"""
        delete from tb_rag_chat_messages
         where session_id = %(session_id)s
    """
    cnt = db.delete(conn, sql, param)
    return dict(cnt=cnt)


# Delete session
@deco.service
@deco.transaction()
def delete_session(conn, param):
    sql = f"""
        delete from tb_rag_chat_sessions
         where id = %(session_id)s
    """
    cnt = db.delete(conn, sql, param)
    return dict(cnt=cnt)


@deco.service
@deco.transaction()
def create_new_prompt(conn, param):

    sql = f"""
        insert into tb_rag_prompt_collection as tp
        (
            prompt_name, prompt_content, description, prompt_type, max_output_token, temperature, topP
        ) values (
            %(prompt_name)s, %(prompt_content)s, %(description)s, %(prompt_type)s, %(max_output_token)s,%(temperature)s,%(topP)s
        )

    """
    cnt = db.save(conn, sql, param)
    logger.debug(f"save.cnt: {cnt}")
    return dict(cnt=cnt)
