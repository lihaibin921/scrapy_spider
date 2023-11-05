# encoding: utf-8
# @Time : 2023/11/5 16:43
# @Auther : ISLEY
# @File : mysql_util.py
# @DESC :
import pymysql
from scrapy_spider.settings import DATABASE_BILI_SETTINGS
import logging

"""
    mysql通用操作类 单例
"""


class MysqlDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MysqlDatabase, cls).__new__(cls)
            cls._instance.conn = pymysql.connect(
                host=DATABASE_BILI_SETTINGS['db_host'],
                port=DATABASE_BILI_SETTINGS['db_port'],
                user=DATABASE_BILI_SETTINGS['db_user'],
                password=DATABASE_BILI_SETTINGS['db_password'],
                database=DATABASE_BILI_SETTINGS['db_name'],
                charset='utf8'  # 注意必须是utf8 不是utf-8
            )
        return cls._instance

    """
        数据库查询
        @query select sql
        @params 
        @return 元组
    """

    def execute_query(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f'sql query error:{e}')
            return ()

    """
        数据库单条增改
        @query sql语句
        @params
    """

    def execute_one(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f'sql execute_one error:{e}')

    """
        数据库批量增改
        @query sql语句
        @params
    """

    def execute_many(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f'sql execute_many error:{e}')

    def close_connection(self):
        self.conn.close()


def test_query():
    db = MysqlDatabase()
    sql = 'SELECT uid FROM bili_user WHERE uid >%s ORDER BY uid  LIMIT %s'
    min_uid = 0
    count = 20
    while min_uid < 200:
        result = db.execute_query(sql, params=(min_uid, count))
        print(result)
        if len(result) > 0:
            min_uid = result[-1][0]
        else:
            break


def test_update_many():
    update_sql = 'UPDATE bili_user SET following = %s , follower = %s WHERE uid = %s'
    datas = [
        (124, 175000, 10001),
        (1, 125, 10002),
        (5, 2852, 10003),
    ]
    db = MysqlDatabase()
    db.execute_many(update_sql, datas)


if __name__ == '__main__':
    test_update_many()
