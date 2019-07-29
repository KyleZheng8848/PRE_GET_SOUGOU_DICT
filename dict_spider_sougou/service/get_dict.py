# -*- coding: utf-8 -*-
# @Time    : 2019/7/26 15:14
# @Author  : ky.zheng
# @File    : get_dict.py
# @description:
# @Software: PyCharm
from tools import *

# 说明：本程序主要是爬取搜狗细胞词库的每一个词库的路径，并形成一个《词库的路径汇总表》文件。

if __name__ == '__main__':
    # parameter
    SELECT_ID = ['城市信息',
                 '自然科学',
                 '社会科学',
                 '工程应用',
                 '农林渔畜',
                 '医学医药',
                 '电子游戏',
                 '艺术设计',
                 '生活百科',
                 '运动休闲',
                 '人文科学',
                 '娱乐休闲']  # 爬取的类别
    ROOT_URL = 'https://pinyin.sogou.com'  # 爬取的网址root
    URL_INDEX = ROOT_URL + '/dict/cate/index/'  # 爬取的index网址
    OP_PATH = '../data/1.path.csv'  # 爬取的数据输出位置

    MAPPING_DICT_CATO = {'城市信息': '167',
                         '自然科学': '1',
                         '社会科学': '76',
                         '工程应用': '96',
                         '农林渔畜': '127',
                         '医学医药': '132',
                         '电子游戏': '436',
                         '艺术设计': '154',
                         '生活百科': '389',
                         '运动休闲': '367',
                         '人文科学': '31',
                         '娱乐休闲': '403'
                         }  # 爬取的类别的index

    # process
    mapping_dict = pd.DataFrame()
    for id_1 in SELECT_ID:
        url_lv1 = URL_INDEX + MAPPING_DICT_CATO[id_1]
        soup_lv1 = url2soup(url_lv1)

        if id_1 == '城市信息':
            mapping_lv2 = index_mapping(soup_lv1, '#city_list_show > table > tbody > tr > td > div a', {})
            for id_2 in mapping_lv2:
                url_lv2 = ROOT_URL + mapping_lv2[id_2]
                soup_lv2 = url2soup(url_lv2)

                mapping_lv3 = index_mapping(soup_lv2, '#dict_cate_show > table > tbody > tr > '
                                                      'td:nth-child(2) > div > a', {})
                for r in range(3, 8):
                    mapping_lv3 = index_mapping(soup_lv2, '#dict_cate_show > table > tbody > tr > '
                                                          'td:nth-child(' + str(r) + ') > div > a', mapping_lv3)
                if id_2 == '国外地名':
                    mapping_lv3 = {id_2: mapping_lv2[id_2]}

                for id_3 in mapping_lv3:
                    url3 = mapping_lv3[id_3]

                    mapping_lv4 = {}
                    while True:
                        url_lv3 = ROOT_URL + url3
                        soup_lv3 = url2soup(url_lv3)
                        requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                           '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                        mapping_lv4 = index_download_mapping(soup_lv3, requirement_lv3, mapping_lv4)

                        page = the_last_element(soup_lv3, '#dict_page_list > ul > li > span > a')
                        if page[0] == '下一页':
                            url3 = page[1]
                        else:
                            break

                    mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv4, orient='index').reset_index()
                    mapping_dict_pre.columns = ['name', 'path']
                    mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2 + '/' + id_3
                    print(id_1, id_2, id_3)

                    if len(mapping_dict) != 0:
                        mapping_dict = mapping_dict.append(mapping_dict_pre)
                    else:
                        mapping_dict = mapping_dict_pre

        elif id_1 == '自然科学':
            have_child_cato = {'物理(34)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(2) > '
                                         'div.cate_children_show > table > tbody > tr > td:nth-child(1) > div > a',
                               '生物(126)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(4) > '
                                          'div.cate_children_show > table > tbody > tr > td:nth-child(1) > div > a'}
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a')
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '社会科学':
            have_child_cato = {'经济管理(140)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                            'div.cate_children_show > table > tbody > tr > td > div > a'}
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '工程应用':
            have_child_cato = {'计算机(258)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                           'div.cate_children_show > table > tbody > tr > td > div > a'}
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '农林渔畜':
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '医学医药':
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '电子游戏':
            have_child_cato = {'单机游戏(240)': '#dict_cate_show > table > tbody > tr > td:nth-child(1) > '
                                            'div.cate_children_show > table > tbody > tr > td > div > a',
                               '网络游戏(888)': '#dict_cate_show > table > tbody > tr > td:nth-child(2) > '
                                            'div.cate_children_show > table > tbody > tr > td > div > a',
                               '网页游戏(71)': '#dict_cate_show > table > tbody > tr > td:nth-child(3) > '
                                           'div.cate_children_show > table > tbody > tr > td > div > a',
                               '手机游戏(131)': '#dict_cate_show > table > tbody > tr > td:nth-child(4) > '
                                            'div.cate_children_show > table > tbody > tr > td > div > a'
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '艺术设计':
            have_child_cato = {'音乐(39)': '#dict_cate_show > table > tbody > tr:nth-child(2) > td:nth-child(3) > '
                                         'div.cate_children_show > table > tbody > tr > td > div > a'
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '生活百科':
            have_child_cato = {'理财(71)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                         'div.cate_children_show > table > tbody > tr > td > div > a'
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '运动休闲':
            have_child_cato = {'球类(68)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                         'div.cate_children_show > table > tbody > tr > td > div > a',
                               '棋牌类(37)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(2) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a'
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '人文科学':
            have_child_cato = {'历史(121)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a',
                               '文学(519)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(2) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a',
                               '语言(162)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(3) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a',
                               '哲学(54)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(4) > '
                                         'div.cate_children_show > table > tbody > tr > td > div > a',
                               '宗教(147)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(5) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a',
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        elif id_1 == '娱乐休闲':
            have_child_cato = {'动漫(337)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(1) > '
                                          'div.cate_children_show > table > tbody > tr > td > div > a',
                               '收藏(22)': '#dict_cate_show > table > tbody > tr:nth-child(1) > td:nth-child(2) > '
                                         'div.cate_children_show > table > tbody > tr > td > div > a'
                               }
            mapping_lv2 = index_mapping(soup_lv1, '#dict_cate_show > table > tbody > tr > td > div > a', {})
            mapping_lv2 = delete_dict_element(mapping_lv2, have_child_cato)
            for c in have_child_cato:
                mapping_lv2 = index_mapping(soup_lv1, have_child_cato[c], mapping_lv2, c)

            for id_2 in mapping_lv2:
                url2 = mapping_lv2[id_2]

                mapping_lv3 = {}
                while True:
                    url_lv2 = ROOT_URL + url2
                    soup_lv2 = url2soup(url_lv2)
                    requirement_lv3 = ['#dict_detail_list > div > div.dict_detail_title_block > div',
                                       '#dict_detail_list > div > div.dict_detail_show > div.dict_dl_btn a']
                    mapping_lv4 = index_download_mapping(soup_lv2, requirement_lv3, mapping_lv3)

                    page = the_last_element(soup_lv2, '#dict_page_list > ul > li > span > a')
                    if page[0] == '下一页':
                        url2 = page[1]
                    else:
                        break

                mapping_dict_pre = pd.DataFrame.from_dict(mapping_lv3, orient='index').reset_index()
                mapping_dict_pre.columns = ['name', 'path']
                mapping_dict_pre['dict_cato'] = id_1 + '/' + id_2
                print(id_1, id_2)

                if len(mapping_dict) != 0:
                    mapping_dict = mapping_dict.append(mapping_dict_pre)
                else:
                    mapping_dict = mapping_dict_pre

        else:
            pass

    write_csv(mapping_dict, OP_PATH)
    print('work finished ! ')





