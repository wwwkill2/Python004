import re
import scrapy
from maoyan.items import MaoyanItem
from scrapy.selector import Selector


class MaoyanmovieSpider(scrapy.Spider):
    name = 'maoyanmovie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)


    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        # 取前10个
        for i in range(10):
            movie = movies[i]
            link = 'https://maoyan.com' + movie.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=link, callback=self.parse2)
    
    def parse2(self, response):
        movie = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        item = MaoyanItem()
        # 电影名称
        title = movie.xpath('./h1/text()')
        # 电影类型
        movie_type = []
        type_selector = movie.xpath('./ul/li[1]/a/text()')
        for t in type_selector:
            movie_type.append(t.get())
        # 上映日期
        play_time = movie.xpath('./ul/li[last()]/text()')
        item['title'] = title.extract_first()
        item['movie_type'] = ''.join(movie_type)
        item['play_time'] = play_time.extract_first()
        yield item

