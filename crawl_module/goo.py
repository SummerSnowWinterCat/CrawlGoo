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
from bs4 import BeautifulSoup as soup
import crawl_module.user_agent_fake as user_fake
import time
import ssl
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
    except Exception:
        print('main service is error!')
    return soup(response, 'lxml')


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
    # for cbw in content_box_word:
    #     print(cbw)
    #    dictionary_index[cbw.li.text] = base_url + cbw.li.a.get('href')
    # cbw.li.text, cbw.li.a.get('href')
    # log here !
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
    except Exception:
        print('pages module is error!')
    return word_pages_url


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
    except Exception:
        print('<word module is error!>')
    return word_dic


# GET IT
def create_database(table_name):
    if len(g_i_d.search_database_table(table_name)) == 0:
        g_i_d.create_all_table()
        return 0
    else:
        print('TABLES  ALL READY!')
        return 0


# insert into database
def syllabary_download(syllabary_list):
    for sl_k, sl_v in tqdm(syllabary_list.items()):
        g_i_d.insert_syllabary_data(str(sl_k), str(sl_v))
    print('syllabary save complete!')

    return 0


def crawl_start(url):
    '''
     crawl_start is to create database_mysql and crawl words
     shell two mode : create init or crawl only
    :return: 0
    '''
    create_database('japanese_syllabary')
    # get request information
    syllabary_list = get_content_box_word(url=url)
    # input to database
    syllabary_download(syllabary_list)
    # get data from mysql
    syllabary_data = g_i_d.search_japanese_syllabary_id_and_url()
    # data reset
    re_syllabary_data = []
    for s_data in syllabary_data:
        # get url from database
        re_data = s_data['URL']
        re_syllabary_data.append((s_data['ID'], re_data))
        for r_s_d in re_syllabary_data:
            r_s_d_id, r_s_d_url = r_s_d[0], r_s_d[1]
            # get id and url
            time.sleep(0.8)
            word_pages_list = get_word_pages(url=r_s_d_url)
            for w_p_l in tqdm(range(len(word_pages_list))):
                url = word_pages_list[w_p_l]
                time.sleep(3.5)
                # get word sleep 3ms
                words_list = get_word(url=url)
                for word, info in words_list.items():
                    word = word.strip()
                    word_meaning = info[0].strip()
                    word_url = info[1].strip()
                    g_i_d.insert_word(word=word, word_url=word_url, word_meaning=word_meaning,
                                      word_update_time=time.strftime(
                                          "%Y-%m-%d %H:%M:%S", time.localtime()), syllabary_id=r_s_d_id)
    return 0
