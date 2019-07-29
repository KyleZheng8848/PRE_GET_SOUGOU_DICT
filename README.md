# 搜狗细胞词库 下载
基于不同广告位策略、时段给予相应的预估流量值

## 功能介绍
- 爬取搜狗细胞词库的每一个词库的路径，并形成一个《词库的路径汇总表》文件。
- 将《词库的路径汇总表》中的词库，根据不同类别，进行下载。
- 将下载后的词库的格式，从secl转换为txt。

## 依赖环境
添加python版本，包依赖版本等其他所用框架版本，格式如下。
- Python-3.6
- pandas-0.25.0
- requests-2.22.0
- bs4-0.1.1

## 使用方式
- 获取《词库的路径汇总表》
- 运行方式

    ```bash
    python get_dict.py
    ```   
- 下载细胞词库
- 运行方式

    ```bash
    python download_dict.py
    ```
- scel转换txt
- 运行方式

    ```bash
    python scel2txt.py
    ```

## 代码结构说明
### 目录结构
此处可以贴一张仓库文件结构图，如下

![目录结构](https://github.com/KyleZheng8848/PRE_GET_SOUGOU_DICT/blob/master/dict_spider_sougou/pic/pic.png?raw=true)

    
### 文件说明
#### service:
- get_dict.py
  获取《词库的路径汇总表》
- download_dict.py
  下载细胞词库
- scel2txt.py
  scel转换txt

#### tools：
- basic.py
  基础函数库
- spider.py
  爬虫相关函数库

## 问题及注意事项
- 暂无

