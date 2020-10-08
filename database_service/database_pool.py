# -*- coding:utf-8 -*-
# @Time : 2020/10/07 20:24
# @Author: WinterCat
# @File : database_pool.py
# @Email:summersnowwintercat@gmail.com

import pymysql
from dbutils.pooled_db import PooledDB
import config


class DataBaseConnectionPool:
    __pool = None

    def __init__(self):
        self.conn = self.get_connection().connection()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_connection(self):
        if self.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                maxconnections=config.DB_MAX_CONNECTIONS,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                ping=config.DB_PING,
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                charset=config.DB_CHARSET
            )
        return __pool

    def __del__(self):
        self.cur.close()
        self.conn.close()


def search_data(query):
    connection = DataBaseConnectionPool()
    connection.cur.execute(query)
    return connection.cur.fetchall()


def add_data(query):
    connection = DataBaseConnectionPool()
    connection.cur.execute(query)
    return connection.conn.commit()
