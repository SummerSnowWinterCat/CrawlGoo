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
import database_mysql.crawl_save as c_save
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
    content_box_word = get_request(url).find_all('ol', class_='list-word cx')
    # into
    for cbw in content_box_word:
        dictionary_index[cbw.li.text] = base_url + cbw.li.a.get('href')
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
def crawl_start(url):
    '''
     crawl_start is to create database_mysql and crawl words
     shell two mode : create init or crawl only
    :return: 0
    '''
    # get request information
    # {'あ': 'https://dictionary.goo.ne.jp/jn/index/%E3%81%82/'
    index_list = get_content_box_word(url=url)
    # init database_mysql
    # print(index_list)
    for t_name, p_url in index_list.items():
        word_pages_list = get_word_pages(p_url)
        for p in tqdm(range(0, len(word_pages_list) + 1)):
            time.sleep(5)
            word_list = get_word(word_pages_list[p])
            for wd, wi, in word_list.items():
                if c_save.save_word(t_name=t_name, word=wd, word_info=wi[0], word_url=wi[1], save_date='now'):
                    continue
                    time.sleep(5)
                else:
                    time.sleep(1)
                    break

    return 0
