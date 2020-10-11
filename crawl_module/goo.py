# coding=utf-8
import os
from urllib import request
import sys
import json
import pprint
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor
from http import cookiejar
import lxml
import pymysql
from bs4 import BeautifulSoup as soup
import crawl_module.user_agent_fake as user_fake
import time
import ssl
import config
import database_service.goo_init_database as g_i_d
from tqdm import tqdm

base_url = 'https://dictionary.goo.ne.jp'


def get_request(url):
    try:
        # ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        # header fake
        headers = {'User-Agent': user_fake.get_fake_header()}
        # get request
        response = request.urlopen(request.Request(url=url, headers=headers)).read().decode('utf8')
        # change to soup
        return soup(response, 'lxml')
    except Exception:
        print('Main Service is Down ')


# 国語DIV
def get_content_box_word(url):
    # create index dic
    dictionary_index = {}
    # get content_box_word
    # print(get_request(url))
    content_box_word = get_request(url).find_all('div', class_='content-box-in col4')
    # into
    for cbw in content_box_word:
        for list_cx in cbw.find_all('ol', class_='list-word cx'):
            for li in list_cx.find_all('li'):
                if li.has_attr('class') is False:
                    dictionary_index[li.text] = base_url + li.a.get('href')

    return dictionary_index


# GET DICTIONARY TO SEARCH WORDS
def get_word_pages(url):
    try:
        # word_pages_url
        word_pages_url = []
        # response hold
        source = get_request(url)
        # last num
        last_num = int(source.find('li', class_='last-num').text)
        # set word url
        [word_pages_url.append(url + str(i)) for i in range(1, last_num + 1)]
        # log here !
        return word_pages_url
    except Exception:
        print('pages module is error!')
        print('URL {}'.format(url))


# GET WORDS
def get_word(url):
    try:
        word_dic = {}
        # response hold
        source = get_request(url)
        # get data
        content_list = source.find('ul', class_='content_list idiom lsize')
        # get data in li
        li_list = content_list.find_all('li')
        # check data
        for i in li_list:
            word_url = base_url + i.a.get('href')
            word_title = i.find(class_='title').text
            word_info = i.find(class_='text').text
            # set into dic
            word_dic[word_title] = (word_info, word_url)
        # log here !
        return word_dic
    except Exception:
        print('<word module is error!>')


# GET IT
def create_database(table_name):
    if len(g_i_d.search_database_table(table_name)) == 0:
        g_i_d.create_all_table()
        return 0
    else:
        print('TABLES  ALL READY!')
        return 0


# insert into database
def insert_data_to_main_table(table_name, data):
    for sl_k, sl_v in tqdm(data.items()):
        g_i_d.insert_main_table_data(syllabary_table_name=table_name, syllabary_data=str(sl_k),
                                     url=str(sl_v))
    print('Main Table save&create complete!')
    return True


def init_crawl():
    g_i_d.drop_schemas(schema_name=config.DB_NAME)
    g_i_d.create_schemas(schema_name=config.DB_NAME)


def download_limit(table_name):
    limit_message = "DOWNLOAD LIMIT (1-{})".format(len(g_i_d.search_main_table_id_and_url(table_name)))
    print(limit_message)
    print('-' * len(limit_message))
    start_id = int(input("START :"))
    end_id = int(input("END :"))
    page_url = {}
    if start_id != end_id:
        for i in range(start_id, end_id + 1):
            page_url[i] = g_i_d.search_main_table_url_by_id(table_name=table_name, id=i)
        return page_url
    else:
        page_url[start_id] = g_i_d.search_main_table_url_by_id(table_name=table_name, id=start_id)
        return page_url


def crawl_start(url):
    _MAIN_TABLE = pymysql.escape_string('japanese_syllabary')
    _WORD_TABLE = 'word_dictionary_'
    _WORD_EXTEND = 'word_extend_'
    '''

    :param url:
    :return:
    '''
    # create main table (key table)
    if g_i_d.create_syllabary_table(_MAIN_TABLE):
        # get request information
        syllabary_list = get_content_box_word(url=url)
        # input to database
        insert_data_to_main_table(_MAIN_TABLE, syllabary_list)
        # get data from mysql
        syllabary_data = g_i_d.search_main_table_id_and_url(_MAIN_TABLE)
        # data reset
        re_syllabary_data = []

        for s_data in syllabary_data:
            # get url from database
            re_data = s_data['URL']
            re_syllabary_data.append((s_data['ID'], re_data))

        for s_i in tqdm(range(1, len(re_syllabary_data) + 1)):
            _WORD_TABLE_R = pymysql.escape_string(_WORD_TABLE + str(s_i))
            _WORD_EXTEND_R = pymysql.escape_string(_WORD_EXTEND + (str(s_i)))
            g_i_d.create_word_table_and_extend(key_table=_MAIN_TABLE, word_table_name=_WORD_TABLE_R,
                                               word_extend_name=_WORD_EXTEND_R)
            time.sleep(0.1)

        print('init complete')

        for k, v in download_limit(table_name=_MAIN_TABLE).items():
            page_list = []
            page_list = get_word_pages(v[0]['URL'])
            for p_index in tqdm(range(0, len(page_list))):
                time.sleep(1.5)
                for w_k, w_v in get_word(page_list[p_index]).items():
                    _word = pymysql.escape_string(w_k)
                    _word_meaning = pymysql.escape_string(w_v[0])
                    _word_url = pymysql.escape_string(w_v[1])
                    _word_table = pymysql.escape_string(_WORD_TABLE + str(k))
                    _word_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    g_i_d.insert_word(table_name=_word_table, word=_word, word_url=_word_url, word_type="",
                                      word_meaning=_word_meaning,
                                      word_update_time=_word_update_time,
                                      syllabary_id=k)
                    time.sleep(0.1)

    else:
        print('Error')


def download_continue():
    _MAIN_TABLE = pymysql.escape_string('japanese_syllabary')
    _WORD_TABLE = 'word_dictionary_'
    _WORD_EXTEND = 'word_extend_'
    for k, v in download_limit(table_name=_MAIN_TABLE).items():
        page_list = []
        page_list = get_word_pages(v[0]['URL'])
        for p_index in tqdm(range(0, len(page_list))):
            time.sleep(1.5)
            for w_k, w_v in get_word(page_list[p_index]).items():
                _word = pymysql.escape_string(w_k)
                _word_meaning = pymysql.escape_string(w_v[0])
                _word_url = pymysql.escape_string(w_v[1])
                _word_table = pymysql.escape_string(_WORD_TABLE + str(k))
                _word_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                g_i_d.insert_word(table_name=_word_table, word=_word, word_url=_word_url, word_type="",
                                  word_meaning=_word_meaning,
                                  word_update_time=_word_update_time,
                                  syllabary_id=k)
                time.sleep(0.1)
    return True
