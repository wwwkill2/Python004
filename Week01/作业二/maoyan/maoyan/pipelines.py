# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class MaoyanPipeline:
    def process_item(self, item, spider):
        # 保存至csv文件
        movie = pd.DataFrame(data=[f'{item["title"]}|{item["movie_type"]}|{item["play_time"]}'])
        movie.to_csv('./maoyan.csv', mode='a', encoding='utf-8', index=False, header=False)
        return item
