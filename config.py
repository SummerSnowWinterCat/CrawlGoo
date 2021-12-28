# -*- coding:utf-8 -*-
# @Time : 2020/10/07 20:36
# @Author: WinterCat
# @File : config.py
# @Email:summersnowwintercat@gmail.com

# DB_CREATOR = 'pymysql'
DB_HOST = '127.0.0.1'
DB_POST = 3306
DB_NAME = 'DICTIONARY'
DB_USER = 'root'
DB_PASSWORD = '000000'

# encode
DB_CHARSET = 'utf8mb4'
#  free cached min
DB_MIN_CACHED = 5
#  free cached max
DB_MAX_CACHED = 20
#  pools create max
DB_MAX_CONNECTIONS = 100
#  share pool max
DB_MAX_SHARED = 20
# max pool block
DB_BLOCKING = True
#  connection use again
DB_MAX_USAGE = 0
#
DB_SET_SESSION = []
#
DB_PING = 0
