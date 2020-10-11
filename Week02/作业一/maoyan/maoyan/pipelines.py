# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : '12345678',
    'db' : 'test'
}

class ConnDB(object):
    def __init__(self, dbInfo):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']

        # self.run()

    def run(self, title, movie_type, play_time):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )
        # 游标建立的时候就开启了一个隐形的事物
        cur = conn.cursor()
        try:
            cur.execute(f'insert into movies values ({title}, {movie_type}, {play_time})')
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()

class MaoyanPipeline:
    def process_item(self, item, spider):
        # 保存至csv文件
        # movie = pd.DataFrame(data=[f'{item["title"]}|{item["movie_type"]}|{item["play_time"]}'])
        # movie.to_csv('./maoyan.csv', mode='a', encoding='utf-8', index=False, header=False)
        # return item
        # 保存至MySQL
        db = ConnDB(dbInfo)
        db.run(item['title'], item['movie_type'], item['play_time'])
