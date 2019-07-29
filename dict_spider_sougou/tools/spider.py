# -*- coding: utf-8 -*-
# @Time    : 2019/7/26 15:14
# @Author  : ky.zheng
# @File    : get_dict.py
# @description:
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from .scel2txt import *
import pandas as pd
import os


def url2soup(request_url):
    res = requests.get(request_url)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def index_mapping(soup, requirement, mapping={}, tag=''):
    raw_data = soup.select(requirement)
    if tag != '':
        tag = tag + '/'
    for r in raw_data:
        index = tag + r.text
        url = r.attrs['href']
        mapping[index] = url
    return mapping


def index_download_mapping(soup, requirement, mapping={}):
    raw_data_index = soup.select(requirement[0])
    raw_data_url = soup.select(requirement[1])

    for r in range(len(raw_data_index)):
        index = raw_data_index[r].text
        url = raw_data_url[r].attrs['href']
        mapping[index] = url
    return mapping


def the_last_element(soup, requirement, stop_word='下一页'):
    index = ''
    url = ''
    raw_data = soup.select(requirement)
    if len(raw_data) != 0:
        index = raw_data[-1].text
    if index == stop_word:
        url = raw_data[-1].attrs['href']
    return index, url


def delete_dict_element(mapping, delete_element):
    for e in delete_element:
        del mapping[e]
    return mapping


def download(dl_path, op_file_path):
    try:
        mapping = requests.get(dl_path)
        with open(op_file_path, "wb") as code:
            code.write(mapping.content)
    except Exception as e:
        print(e)


