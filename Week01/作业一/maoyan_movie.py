from sys import platform
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

header = {'User-Agent': user_agent}

url_prefix = 'https://maoyan.com'

start_url = 'https://maoyan.com/films?showType=3'

cookies = {'__mta': '120951607.1601185963515.1601189003222.1601189286732.6', 'uuid_n_v': 'v1', 'uuid': 'A0AACA90008511EBAAFDB3416A6201C80CCFAFF7FF1F4945A8AC395C3F6A3549', '_csrf': 'f5d31038520393cc4dfe501174c655a8b91fec31dca9991a3ec9c17020442b0f', 'mojo-uuid': '4dfc676dae39defa5252e04fc0d81b67', 'mojo-session-id': '{"id":"1f87f5123f9e1d7c28a20e117307d9b1","time":1601185951048}',
           '_lxsdk_cuid': '174ce1edc3ac8-0f78d4f54f49bc-31697304-1aeaa0-174ce1edc3ac8', '_lxsdk': 'A0AACA90008511EBAAFDB3416A6201C80CCFAFF7FF1F4945A8AC395C3F6A3549', 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1601185950,1601185997,1601189058', 'mojo-trace-id': '11', 'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1601189286', '_lxsdk_s': '174ce1edc3b-12e-d5f-bcb%7C%7C18'}

my_movie_data = []


def get_movie_list():
    # 请求电影列表
    response = requests.get(start_url, headers=header, cookies=cookies)
    print(response.text)
    # 初始化BeautifulSoup对象
    bs_info = bs(response.text, 'html.parser')
    # 获取当前页面全部的电影标签
    tags = bs_info.find_all('div', attrs={'class': 'movie-item'})
    # 按照题目要求，取前十个
    for i in range(10):
        tag = tags[i]
        # 找到第一个a标签
        atag = tag.find('a')
        # 取a标签的超链接
        href = atag.get('href')
        # 拼接超链接，发起电影详情请求
        href = url_prefix + href
        get_movie_detail(href)
        # 每次请求间隔1秒，防止爬虫被禁
        time.sleep(1)


def get_movie_detail(href):
    response = requests.get(href, headers=header)
    bs_info = bs(response.text, 'lxml')
    tag = bs_info.find('div', attrs={'class': 'movie-brief-container'})
    # 电影名称
    title = tag.find('h1').string
    # 找到所有的li标签
    lis = tag.find_all('li', attrs={'class': 'ellipsis'})
    # 电影类型
    atags = lis[0].find_all('a')
    movie_type = []
    for atag in atags:
        movie_type.append(atag.string)
    # 上映时间
    play_time = lis[-1].string
    my_movie_data.append(f'{title}|{"".join(movie_type)}|{play_time}')


def save_csv():
    movie = pd.DataFrame(data=my_movie_data)
    movie.to_csv('./maoyan.csv', encoding='utf-8', index=False, header=False)


if __name__ == '__main__':
    get_movie_list()
    save_csv()
