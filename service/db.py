from typing import List

import loguru
from mysql.connector import MySQLConnection, connect
from logs import logger
from utils.config import DATABASE_DB


class MysqlDb:
    default_db_settings = DATABASE_DB

    def __init__(self):
        pass

    def __enter__(self):
        self._conn: MySQLConnection = self._get_connect(**self.default_db_settings)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    @property
    def conn(self):
        return self._conn

    def _get_connect(self, host: str = None,
                     port: int = None,
                     user: str = None,
                     passwd: str = None,
                     db: str = None,
                     ) -> MySQLConnection:
        """获取数据库连接
        :return:
        """

        conn = connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
        )
        return conn

    def insert_many_data(self, sql_list: list):
        cursor = self._conn.cursor()
        for sql in sql_list:
            cursor.execute(sql)
            self._conn.commit()
            logger.debug(f"开始插入数据库-{sql}")
