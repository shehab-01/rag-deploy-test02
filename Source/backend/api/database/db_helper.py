import re
import atexit
import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection, cursor
from typing import Generator, Union
from contextlib import contextmanager
import faiss
import pickle
import io
import numpy as np
from langchain.schema import Document
from typing import List

from api.utils.logger import logger
from api.common import exceptions as ex
from api.common.settings import settings
from api.rag.nlu import process_query_nlu
from api.rag.embedding import get_embedding_function


class DBHelper:
    def __init__(self):
        logger.info("DBHelper.__init__")
        self._connection_pool = None
        # self.initialize_connection_pool()

    def initialize_connection_pool(self):
        logger.info("Connection pool initialize..")
        try:
            type = "default"
            self._connection_pool = pool.ThreadedConnectionPool(
                # 5,  # minConnection
                # 10,  # maxConnection
                # connect_timeout=0,
                minconn=settings.Config.database["POOL-MIN"],
                maxconn=settings.Config.database["POOL-MAX"],
                host=settings.Config.database["HOST"],
                port=settings.Config.database["PORT"],
                database=settings.Config.database["NAME"],
                user=settings.Config.database["USER"],
                password=settings.Config.database["PASSWORD"],
                options="-c search_path=maxted,'$user',public",
            )
            # conn: connection = self._connection_pool.getconn()

            if self._connection_pool:
                logger.info("Connection pool created successfully")
            else:
                raise ex.DBFailureEx(detail="Connection pool created fail")

        except (Exception, psycopg2.Error) as e:
            raise ex.DBFailureEx(ex=e, detail="Error while connecting to Database.")

    def get_connection_pool(self) -> pool.ThreadedConnectionPool:
        try:
            if self._connection_pool is None:
                self.initialize_connection_pool()
            return self._connection_pool
        except Exception as e:
            raise ex.DBFailureEx(ex=e, detail="Error while execute to Database.")

    def get_connection(self) -> Generator:
        try:
            if self._connection_pool is None:
                self.initialize_connection_pool()

            # psycopg2.extensions.connection
            conn: connection = self._connection_pool.getconn()
            conn.autocommit = False
            yield conn
        except Exception as e:
            raise ex.DBFailureEx(ex=e, detail="Error while execute to Database.")
        finally:
            self._connection_pool.putconn(conn)  # 연결반환

    @contextmanager
    def get_conn(self, autocommit=False) -> Generator:
        try:
            if self._connection_pool is None:
                self.initialize_connection_pool()

            # psycopg2.extensions.connection
            conn: connection = self._connection_pool.getconn()
            conn.readonly = None
            conn.autocommit = autocommit
            cursor = conn.cursor()
            yield conn, cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ex.DBFailureEx(ex=e, detail="Error while execute to Database.")
        finally:
            cursor.close()
            self._connection_pool.putconn(conn)  # 연결반환

    def shutdown_connection_pool(self):
        logger.info("Connection pool closeall..")
        if self._connection_pool is not None:
            self._connection_pool.closeall()
            self._connection_pool = None

    def create_rag_vectors_table(self):
        logger.info("Creating rag_vectors table if not exists")
        try:
            with self.get_conn(autocommit=True) as (conn, cur):
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS rag_vectors (
                        id SERIAL PRIMARY KEY,
                        full_path TEXT UNIQUE NOT NULL,
                        faiss_index BYTEA,
                        pkl_file BYTEA,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
            logger.info("rag_vectors table created successfully")
        except Exception as e:
            logger.error(f"Error in create_rag_vectors_table: {str(e)}")
            raise ex.DBFailureEx(ex=e, detail="Error while creating rag_vectors table.")

    def add_to_postgres_faiss(self, full_path: str, faiss_index: bytes, pkl_file: bytes):
        logger.info(f"Storing FAISS index for {full_path}")
        try:
            with self.get_conn() as (conn, cur):
                cur.execute(
                    """
                    INSERT INTO rag_vectors (full_path, faiss_index, pkl_file)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (full_path) 
                    DO UPDATE SET 
                        faiss_index = EXCLUDED.faiss_index,
                        pkl_file = EXCLUDED.pkl_file,
                        updated_at = CURRENT_TIMESTAMP
                """,
                    (full_path, psycopg2.Binary(faiss_index), psycopg2.Binary(pkl_file)),
                )

            logger.info(f"FAISS index for {full_path} stored successfully")
            return f"Vectors for {full_path} stored in PostgreSQL"
        except Exception as e:
            logger.error(f"Error in add_to_postgres_faiss: {str(e)}")
            raise ex.DBFailureEx(
                status_code=500, msg="[DB] 내부 서버 오류입니다.", detail=f"Error while storing vectors in Database: {str(e)}", code="5000002", ex=e
            )

    def load_faiss_from_postgres(self, full_path: str):
        logger.info(f"Loading FAISS index for {full_path}")
        try:
            with self.get_conn() as (conn, cur):
                cur.execute(
                    """
                    SELECT faiss_index, pkl_file
                    FROM rag_vectors
                    WHERE full_path = %s
                """,
                    (full_path,),
                )

                result = cur.fetchone()
                if result is None:
                    raise ValueError(f"No data found for path: {full_path}")

                faiss_bytes, pkl_bytes = result

                logger.info(f"FAISS index for {full_path} loaded successfully")
                return faiss_bytes, pkl_bytes
        except Exception as e:
            logger.error(f"Error in load_faiss_from_postgres: {str(e)}")
            raise ex.DBFailureEx(ex=e, detail="Error while loading vectors from Database.")


db_helper = DBHelper()


async def process_query(query_text: str, selected_path: str, question_language: str):
    nlu_result = process_query_nlu(query_text, question_language)
    query_language = nlu_result["language"]

    # Load merged FAISS index and metadata from PostgreSQL for the selected path
    index, metadata = db_helper.load_merged_faiss_from_postgres(selected_path)

    # Get document language from metadata (assuming all files have the same language)
    document_language = metadata[0]["language"]
    embedding_function = get_embedding_function(document_language)

    # Perform similarity search across all files in the selected path
    query_vector = embedding_function.embed_query(query_text)
    D, I = index.search(np.array([query_vector]), k=20)  # Adjust k as needed

    # Get the relevant documents from all files in the selected path
    relevant_docs = [Document(page_content="", metadata=metadata[i]) for i in I[0]]

    # Here you would typically process these relevant documents to generate an answer
    # For this example, we'll just return the top 3 most relevant document metadata
    top_results = relevant_docs[:3]

    result = {
        "query": query_text,
        "selected_path": selected_path,
        "top_results": [
            {"full_path": doc.metadata["full_path"], "page": doc.metadata.get("page", "N/A"), "similarity_score": float(D[0][i])}
            for i, doc in enumerate(top_results)
        ],
        "nlu_info": nlu_result,
    }

    return result


# @atexit.register
# def shutdown_connection_pool():
#     db_helper.shutdown_connection_pool()


""""""


class DB:
    """
    cursor.fetch: 반환값에 column-key가 없어 description 참조하여 재작성
    """

    ##################################################################################
    # Helper functions for dictfetch* for databases that don't natively support them #
    ##################################################################################
    def _dict_helper(self, desc, row) -> dict:
        "Returns a dictionary for the given cursor.description and result row."
        return dict(zip([col[0] for col in desc], row))

    # def dictfetchone(self, cursor: cursor) -> tuple:
    #     "Returns a row from the cursor as a dict"
    #     row = cursor.fetchone()
    #     if not row:
    #         return None
    #     desc = cursor.description
    #     return self._dict_helper(desc, row)

    # def dictfetchall(self, cursor: cursor) -> list:
    #     "Returns all rows from a cursor as a dict"
    #     desc = cursor.description
    #     for row in cursor.fetchall():
    #         yield self._dict_helper(desc, row)

    def dictfetchone(self, cursor: cursor) -> tuple:
        "Returns a rows from a cursor as a dict"
        desc = cursor.description
        row = cursor.fetchone()
        if row is not None:
            return dict(zip([col[0] for col in desc], row))
        return None

    def dictfetchall(self, cursor: cursor) -> list:
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        rows = cursor.fetchall()
        if rows is not None:
            return [dict(zip([col[0] for col in desc], row)) for row in rows]
        return None

    def dictfetchmany(self, cursor: cursor, number: int) -> list:
        "Returns a certain number of rows from a cursor as a dict"
        desc = cursor.description
        rows = cursor.fetchmany(number)
        if rows is not None:
            return [dict(zip([col[0] for col in desc], row)) for row in rows]
        return None

    def sql_print(self, cursor: cursor):
        sql = str(cursor.query, encoding="UTF-8")
        logger.debug(f"sql: {sql}")

    def sql_parse(self, cursor: cursor, sql: str, param: dict) -> str:
        query = None
        try:
            query = cursor.mogrify(sql, param)
        except KeyError as ke:
            key = re.sub("(')|(\")", "", str(ke))
            param[key] = None
            query = self.sql_parse(cursor, sql, param)
        except Exception as ex:
            raise ex
        return query

    def execute(self, cursor: cursor, sql: str, param=None):
        # cursor.execute(sql)
        cursor.execute(sql, param)

    def selectOne(self, conn: connection, sql: str, param=None) -> tuple:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        row = self.dictfetchone(cursor)
        self.sql_print(cursor)
        return row

    def selectList(self, conn: connection, sql: str, param=None) -> list:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        rows = self.dictfetchall(cursor)
        self.sql_print(cursor)
        return rows

    def selecFetch(self, conn: connection, sql: str, param=None, num=None) -> list:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        rows = self.dictfetchmany(cursor, num)
        self.sql_print(cursor)
        return rows

    def selectPaging(self, conn: connection, sql: str, param=None) -> list:
        rows = None
        if param.get("pageSize") and param.get("pageNumber"):
            cursor = conn.cursor()
            paging_sql = f"""
                select count(1) over() as cnt
                    , row_number(*) over() as rn
                    , paging.*
                from (
                    {sql}
                ) as paging
                limit %(pageSize)s offset (%(pageNumber)s - 1) * %(pageSize)s
            """
            query = self.sql_parse(cursor, paging_sql, param)
            cursor.execute(query)
            rows = self.dictfetchall(cursor)
            self.sql_print(cursor)
        return rows

    def save(self, conn: connection, sql: str, param=None) -> int:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        self.sql_print(cursor)
        return cursor.rowcount

    def insert(self, conn: connection, sql: str, param=None) -> int:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        self.sql_print(cursor)
        return cursor.rowcount

    def update(self, conn: connection, sql: str, param=None) -> int:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        self.sql_print(cursor)
        return cursor.rowcount

    def delete(self, conn: connection, sql: str, param=None) -> int:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        self.sql_print(cursor)
        return cursor.rowcount

    def insertFetch(self, conn: connection, sql: str, param=None) -> tuple:
        cursor = conn.cursor()
        query = self.sql_parse(cursor, sql, param)
        cursor.execute(query)
        row = self.dictfetchone(cursor)
        self.sql_print(cursor)
        return row


db = DB()
