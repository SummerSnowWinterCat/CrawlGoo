# -*- coding:utf-8 -*-
# @Time : 2020/10/07 20:24
# @Author: WinterCat
# @File : database_pool.py
# @Email:summersnowwintercat@gmail.com
from database_service.database_pool import search_data, add_data
import time
import pymysql


# create main key table
def create_syllabary_table(table_name):
    _SYLLABARY_SQL = '''
            CREATE TABLE IF NOT EXISTS {}(
            ID INT PRIMARY KEY AUTO_INCREMENT,
            SYLLABARY VARCHAR(25) NOT NULL,
            URL VARCHAR(1000)
            )CHARSET utf8mb4;
            '''.format(table_name)

    if len(search_database_table(table_name)) == 0:
        if add_data(query=_SYLLABARY_SQL) != -1:
            print('Create {} SUCCESS'.format(table_name))
            return True
        else:
            print('Create {} Error'.format(table_name))
            return False
    else:

        print('{} is STANDBY'.format(table_name))
        return True


# CREATE BASE WORD TABLE
def create_word_table_and_extend(word_table_name, key_table, word_extend_name):
    _WORD_SQL = '''
      CREATE TABLE IF NOT EXISTS {}(
      ID INT PRIMARY KEY AUTO_INCREMENT,
      WORD VARCHAR(200) NOT NULL ,
      WORD_TYPE VARCHAR(200),
      WORD_URL VARCHAR(1000) NOT NULL ,
      WORD_MEANING VARCHAR(2000),
      UPDATE_TIME DATETIME,
      SYLLABARY_ID INT NOT NULL ,
      FOREIGN KEY (SYLLABARY_ID) references {}(ID))
      CHARSET utf8mb4;
    '''.format(word_table_name, key_table)

    _WORD_EXTEND = '''
    CREATE TABLE IF NOT EXISTS {}(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    WORD_MEANING VARBINARY(7000),
    UPDATE_TIME DATETIME,
    WORD_ID INT,
    FOREIGN KEY (WORD_ID) references {}(ID))
    CHARSET utf8mb4;
    '''.format(word_extend_name, word_table_name)
    if add_data(query=_WORD_SQL) != -1:
        if add_data(query=_WORD_EXTEND) != -1:
            return True
        else:
            print('Create {} ERROR!'.format(word_extend_name))
            return False
    else:
        print('Create {} Table ERROR!'.format(word_table_name))
        return False


def create_word_index_dictionary(word_index_dictionary_name):
    word_index_dictionary = '''
           CREATE TABLE IF NOT EXISTS '{}'(
         ID INT PRIMARY KEY AUTO_INCREMENT,
         WORD VARCHAR(200) NOT NULL ,
         WORD_TYPE VARCHAR(100),
         WORD_URL VARCHAR(1000) NOT NULL ,
         WORD_MEANING VARCHAR(2000),
         UPDATE_TIME DATETIME,
         SYLLABARY_ID INT NOT NULL ,
         FOREIGN KEY (SYLLABARY_ID) references japanese_syllabary(ID))
         CHARSET utf8mb4;
       '''.format(word_index_dictionary_name)
    result = add_data(word_index_dictionary)
    if result != -1:
        return True
    else:
        return False


# main table insert
def insert_main_table_data(syllabary_table_name, syllabary_data, url):
    if syllabary_data is not None:
        sql = '''
            INSERT INTO {} (ID, SYLLABARY,URL) VALUES (null,'{}','{}');
        '''.format(syllabary_table_name, syllabary_data, url)
        return add_data(query=sql)
    else:
        return False


def insert_word(table_name, word, word_url, word_type, word_meaning, word_update_time, syllabary_id):
    sql = '''
    INSERT INTO {}(ID,WORD,WORD_TYPE,WORD_URL,WORD_MEANING,UPDATE_TIME,SYLLABARY_ID)
    VALUES (null,'{}','{}','{}','{}','{}','{}');
    '''.format(table_name, word, word_type, word_url, word_meaning, word_update_time, syllabary_id)
    return add_data(query=sql)


def insert_word_extend(word_meaning, word_update_time, word_id):
    word_meaning = pymysql.escape_string(word_meaning)
    sql = '''
    INSERT INTO word_extend(ID,WORD_MEANING,UPDATE_TIME,WORD_ID)
    VALUES (null,'{}','{}','{}');
    '''.format(word_meaning, word_update_time, word_id)
    return add_data(query=sql)


def search_database_table(table_name):
    sql = '''
     SHOW TABLES like '{}';
    '''.format(table_name)
    return search_data(query=sql)


def search_main_table_id_and_url(table_name):
    sql = '''
       SELECT ID,URL FROM {};
    '''.format(table_name)
    return search_data(query=sql)


def search_main_table_url_by_id(table_name, id):
    sql = '''
    SELECT URL FROM {} WHERE ID= {};
    '''.format(table_name, id)
    return search_data(query=sql)


def drop_schemas(schema_name):
    sql = '''
        DROP schema {};
    '''.format(pymysql.escape_string(schema_name))
    add_data(sql)
    return True


def create_schemas(schema_name):
    sql = '''
        CREATE SCHEMA {};
    '''.format(pymysql.escape_string(schema_name))
    add_data(sql)
    return True
