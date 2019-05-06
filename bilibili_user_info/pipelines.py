# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BilibiliUserInfoPipeline(object):
    def process_item(self, item, spider):
        return item


from openpyxl import Workbook
from scrapy.conf import settings
class XlxsPipeline(object):  # 设置工序一
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['用户mid号', '用户名', '视频', '用户URL'])  # 设置表头


    def process_item(self, item, spider):  # 工序具体内容
        line = [item['user_mid'], item['user_uname'], item['movies'], item['user_url']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('movies.xlsx')  # 保存xlsx文件
        return item



import codecs
import json
import os
class CsvPipeline(object):
    def __init__(self):
        # w 写文件
        # w+ 读写文件 r 读  r+ 读写文件
        # 前者读写文件，如果文件不存建，则创建
        # 后者读写文件，如果不存在，则抛出异常
        self.file = codecs.open('book.json', 'w+', encoding='utf-8')

    # 如果想要将数据写入本地 或者想将数据写入数据库的时候，这个方法保留
    def process_item(self, item, spider):
        # 将item对象转化为字典对象
        res = dict(item)

        # dumps 将字段对象转化为字符串， ascii编码是否可用
        # 如果直接将字典形式的数据写入到文件当中，会发生错误，所以讲字典形式的值，转化为字符串形式，写入到文件中
        str = json.dumps(res, ensure_ascii=False)
        # 将数据写入到文件当中
        self.file.write(str)
        self.file.write(',\n')


import pymongo
from scrapy.conf import settings



class MongdbPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
