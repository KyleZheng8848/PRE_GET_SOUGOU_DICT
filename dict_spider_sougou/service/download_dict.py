# -*- coding: utf-8 -*-
# @Time    : 2019/7/26 15:14
# @Author  : ky.zheng
# @File    : download_dict.py
# @description:
# @Software: PyCharm
from tools import *
import os

# 说明：本程序主要是将《词库的路径汇总表》中的词库，根据不同类别，进行下载。

if __name__ == '__main__':
    ROOT_PATH = '../data/'
    IP_PATH = ROOT_PATH + '1.path1.csv'
    dict_menu = read_csv(IP_PATH)
    dict_menu = dict_menu.values

    for dm in dict_menu:
        dl_path = dm[1]
        op_path = ROOT_PATH + 'dicts/' + dm[2]
        op_file_path = op_path + '/' + dm[0] + '.scel'

        isExists = os.path.exists(op_path)
        if not isExists:
            os.makedirs(op_path)

        dict_file = download(dl_path, op_file_path)
        print(dm[0], 'has download !')
