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
from database_service.database_pool import search_data, add_data
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


# it dicitionary
def get_url_limit():
    url = 'https://dictionary.goo.ne.jp/jn/category/IT%E7%94%A8%E8%AA%9E/'
    soup_data = get_request(url)
    url_list = []
    li = soup_data.find('li', class_='last-num')
    limit_num = int(li.text)
    for i in range(1, limit_num + 1):
        url_list.append(url + (str(i)))
    return url_list


# get word list
def get_word_list(url):
    word_list = []
    data = get_request(url)
    ul_list = (data.find('ul', class_='content_list idiom lsize'))
    for i in ul_list.find_all('li'):
        word_list.append([base_url + i.a.get('href'), i.text])
    return word_list


# get word contents return dic
def get_word_contents(url, word):
    word = word.replace('\n\n', '')
    # result  = { word , url , update time, meaning )
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = {}
    data = get_request(url)
    contents_list = data.find_all('div', class_='contents')
    contents = ''
    for c in contents_list:
        contents += c.text
    result['WORD'] = word
    result['UPDATETIME'] = update_time
    result['MEANING'] = contents
    result['INITIALS'] = word[0]
    result['URL'] = url
    return result


def insert_into_db(**data):
    word = data.get('WORD')
    url = pymysql.escape_string(data.get('URL'))
    meaning = pymysql.escape_string(data.get('MEANING'))
    updatetime = data.get('UPDATETIME')
    initials = pymysql.escape_string(data.get('INITIALS'))
    _QUERY = '''
        INSERT INTO {}(ID,INITIALS,WORD,MORPHEME,URL,MEANING,UPDATETIME,EXTEND)
        VALUES (null,'{}','{}',null ,'{}','{}','{}',null);
        '''.format('DICTIONARY_IT', pymysql.escape_string(initials), pymysql.escape_string(word),
                   pymysql.escape_string(url),
                   pymysql.escape_string(meaning), updatetime)
    return add_data(query=_QUERY)


if __name__ == '__main__':
    '''
        try:
        for page in tqdm(get_url_limit()):
            time.sleep(0.1)
            for w_l in tqdm(get_word_list(page)):
                data = get_word_contents(w_l[0], w_l[1])
                insert_into_db(**data)
    except Exception:
        print('ERROR')
        print(page)
        print(w_l)
        print('break')
    
    '''

