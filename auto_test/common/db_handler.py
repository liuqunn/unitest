#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 21:14
# @Author : 心蓝
import pymysql


class DB:
    def __init__(self, db_config: dict):
        # 创建连接
        self.conn = pymysql.connect(**db_config)

    def get_one(self, sql):
        """
        获取一条数据
        :param sql:
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def get_many(self, sql, size: int):
        """
        获取多条数据
        :param sql:
        :param size:
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchmany(size)

    def get_all(self, sql):
        """
        获取所有数据
        :param sql:
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def exist(self, sql):
        """
        是否存在数据
        :param sql:
        :return:
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            if cursor.fetchone():
                return True
            else:
                return False

    def __del__(self):
        """
        忘记关闭连接的时候关闭连接
        :return:
        """
        self.conn.close()


if __name__ == '__main__':
    import settings
    db = DB(settings.DB_CONFIG)
    sql = 'select id, reg_name from member limit 10'
    res = db.get_one(sql)
    print(res)
    res = db.get_many(sql,2)
    print(res)
    res = db.get_all(sql)
    print(res)
    res = db.exist(sql)
    print(res)