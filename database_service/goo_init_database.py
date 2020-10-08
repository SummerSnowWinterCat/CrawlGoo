# -*- coding:utf-8 -*-
# @Time : 2020/10/07 20:24
# @Author: WinterCat
# @File : database_pool.py
# @Email:summersnowwintercat@gmail.com
from database_service.database_pool import search_data, add_data
import time
import pymysql


def create_all_table():
    '''
    this function is to create key table
    -ID- -KEY-
    -ID- -WORD- -WORD_INFO- -URL- -DATETIME- -KEY_ID-
    -ID- -WORD_INFO- -DATETIME- -URL- -WORD-ID-
    :return: result
    '''
    syllabary_sql = '''
    CREATE TABLE IF NOT EXISTS japanese_syllabary(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    SYLLABARY VARCHAR(25) NOT NULL,
    URL VARCHAR(1000)
    )CHARSET utf8;
    '''

    word_sql = '''
        CREATE TABLE IF NOT EXISTS word_dictionary(
      ID INT PRIMARY KEY AUTO_INCREMENT,
      WORD VARCHAR(200) NOT NULL ,
      WORD_URL VARCHAR(1000) NOT NULL ,
      WORD_MEANING VARCHAR(2000),
      UPDATE_TIME DATETIME,
      SYLLABARY_ID INT NOT NULL ,
      FOREIGN KEY (SYLLABARY_ID) references japanese_syllabary(ID))
      CHARSET utf8mb4;
    '''

    word_extend_sql = '''
    CREATE TABLE IF NOT EXISTS word_extend(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    WORD_MEANING VARBINARY(7000),
    UPDATE_TIME DATETIME,
    WORD_ID INT,
    FOREIGN KEY (WORD_ID) references word_dictionary(ID))
    CHARSET utf8mb4;  
    '''
    try:
        syllabary_result, word_result, word_extend_result = -1, -1, -1
        syllabary_result = add_data(query=syllabary_sql)
        if syllabary_result != -1:
            word_result = add_data(query=word_sql)
        if word_result != -1:
            word_extend_result = add_data(query=word_extend_sql)
        if word_extend_result != -1:
            return True
        else:
            return False
    except Exception:
        print('database init error')


def insert_syllabary_data(syllabary_data, url):
    if syllabary_data is not None:
        sql = '''
            INSERT INTO japanese_syllabary(ID, SYLLABARY,URL) VALUES (null,'{}','{}');
        '''.format(syllabary_data, url)
        return add_data(query=sql)
    else:
        return False


def insert_word(word, word_url, word_meaning, word_update_time, syllabary_id):
    word, word_url, word_meaning = pymysql.escape_string(word), pymysql.escape_string(word_url), pymysql.escape_string(
        word_meaning)

    sql = '''
    INSERT INTO word_dictionary(ID,WORD,WORD_URL,WORD_MEANING,UPDATE_TIME,SYLLABARY_ID)
    VALUES (null,'{}','{}','{}','{}','{}');
    '''.format(word, word_url, word_meaning, word_update_time, syllabary_id)
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


def search_japanese_syllabary_id_and_url():
    sql = '''
       SELECT ID,URL  FROM japanese_syllabary;
    '''
    return search_data(query=sql)
