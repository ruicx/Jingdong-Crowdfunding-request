
# -*- coding: utf-8 -*-

'''
name:       串行爬虫
usage:      --
author:     [[
date:       2017/11/08 16:55:06
version:    1.0

'''

# %% 导入模块

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


# %% 定义函数与结果数据框

totalPage = 100
stratPage = 51

colName = ['title', 'money', 'progress', 'NoFsupportors',
           'price1', 'sold1', 'total1', 'intro1',
           'price2', 'sold2', 'total2', 'intro2',
           'price3', 'sold3', 'total3', 'intro3',
           'price4', 'sold4', 'total4', 'intro4',
           'price5', 'sold5', 'total5', 'intro5',
           'price6', 'sold6', 'total6', 'intro6',
           'price7', 'sold7', 'total7', 'intro7',
           'price8', 'sold8', 'total8', 'intro8',
           'price9', 'sold9', 'total9', 'intro9',
           'price10', 'sold10', 'total10', 'intro10',
           'price11', 'sold11', 'total11', 'intro11',
           'price12', 'sold12', 'total12', 'intro12',
           'price13', 'sold13', 'total13', 'intro13',
           'price14', 'sold14', 'total14', 'intro14',
           'price15', 'sold15', 'total15', 'intro15',
           'price16', 'sold16', 'total16', 'intro16',
           'price17', 'sold17', 'total17', 'intro17',
           'price18', 'sold18', 'total18', 'intro18',
           'price19', 'sold19', 'total19', 'intro19',
           'price20', 'sold20', 'total20', 'intro20']

rsl = pd.DataFrame(columns=colName)


def asDataFrame(info, detail):
    data = info + detail
    for aa in range(len(data), 4 * (1 + 20)):
        data.append('')
    rsl = pd.DataFrame([data], columns=colName)
    # print(rsl)
    return rsl


# %% 获取链接

# 开始的URL地址
all_url = 'https://z.jd.com/bigger/search.html'

# 正则模板
linkSearch = re.compile(r'href="([^"]*)"')

# 链接储存
urls = []           # 要访问的链接
failUrl = []        # 失败的链接

# 计时器初始化
tic = time.time()

# 计数器初始化
count = 1

for index, aa in enumerate(range(stratPage, totalPage + 1)):
    # 请求
    start_html = requests.post(
        all_url,
        data={'page': str(aa), 'sort': 'zhtj', 'categoryId': '10'}
        )

    # 解析网页
    Soup = BeautifulSoup(start_html.text, 'lxml')

    # 获取全部链接
    links = Soup.find_all('div', class_='i-tits')

    for link in links:
        url = r'https://z.jd.com' + linkSearch.search(str(link)).group(1)
        urls.append(url)

    print(index, '已经过去', time.time() - tic, 's')


# %% 抓取网页

# 浏览器请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64)\ AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    }

for url in urls:
    try:

        # 使用requests中的get方法来获取all_url
        start_html = requests.get(url, headers=headers)

        # 解析网页
        Soup = BeautifulSoup(start_html.text, 'lxml')

        # 获取内容
        tit = Soup.find('p', class_='p-title').get_text()
        money = Soup.find('p', class_='p-num').get_text()
        progress = Soup.find('span', class_='fl').get_text()
        supportor = Soup.find('span', class_='fr').get_text()

        info = [tit, money, progress, supportor]
        costDetails = []
        projectDetails = Soup.find_all('div', class_="box-grade")

        for index, detail in enumerate(projectDetails[0:-6]):

            temp = detail.find('div', class_='t-price').span.get_text()
            price = int(re.findall('\d+', temp)[0])

            temp = detail.find('div', class_='t-people').span.get_text()
            sold = int(re.findall('\d+', temp)[0])

            total = detail.find('span', class_='limit-num').get_text()

            temp = detail.find('p', class_='box-intro').get_text()
            intro = re.sub(' |\\r|\\n|\\t', '', temp)

            costDetails += [price] + [sold] + [total] + [intro]

        rsl = rsl.append(asDataFrame(info, costDetails))
        print(count, '已经过去', time.time() - tic, 's')
        count += 1

    except:
        failUrl.append(url)
        print(url)


# %% 存入excel

# 对齐数据
rsl.index = range(len(rsl))
rsl = rsl.ix[:, colName]

# 记录数据
rsl.to_excel("科技类%d-%d页结果.xlsx" % (stratPage, totalPage))
pd.DataFrame(failUrl).to_csv('科技类%d-%d页fialUrl.csv' % (stratPage, totalPage))
