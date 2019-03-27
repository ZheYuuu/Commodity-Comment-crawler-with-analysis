# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:getCommodityInfo.py
@time:2019/3/1914:13
"""

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from JDSpider.items import JDCommodityItem
from django.views.decorators.csrf import csrf_exempt


'''
    根据搜索关键词获得京东相应商品信息
'''

class GetCommodityInfo(scrapy.Spider):
    name = "getCommodityInfo"
    def __init__(self,*args,**kwargs):
        self.searchKey = kwargs.get('searchKey')
        self.category = kwargs.get('category')
        self.bashUrl = self.bashUrl = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' \
                        '&qrst=1&rt=1&stop=1&vt=2&s=54&click=0&page=' % self.searchKey
        self.num = int(kwargs.get('num'))
        print("Spider has been initiated!",self.searchKey,self.category)

    def start_requests(self):
        # Test Sample
        # self.searchKey = "switch"
        # self.category = "electronic"
        url = self.bashUrl + "1"
        yield Request(url,callback=self.parse)

    def parse(self, response):
        # 获取原始网页信息
        bs = BeautifulSoup(response.text)

        # 获取品牌列表
        try:
            brandList = bs.find('ul', 'J_valueList')
            tmp = brandList.find_all('a')
            brands = [s['title'].split('（')[0] for s in tmp]
        except:
            brandList = []
            print("未获取到商品品牌信息")
        # 翻页爬取商品数据, 一页有60个商品,起始页为1,网站为ajax动态加载，所以页码数为2*i+1
        maxPage = (self.num-1)//60 + 1
        for i in range(0,maxPage):
            url = self.bashUrl + str(2*i+1)
            yield Request(url, callback=self.getItemList, meta={'brand_list': brands},dont_filter=True)

    def getItemList(self,response):
        bs = BeautifulSoup(response.text)
        goods_list = bs.find_all('li', 'gl-item')
        pattern = re.compile('|'.join(response.meta['brand_list']))
        for goods in goods_list:
            item = JDCommodityItem()
            # searchKey 未定义
            try:
                item['searchKey'] = self.searchKey
                item['price'] = float(goods.find('div','p-price').find('i').text.strip())
                name = goods.find('div', 'p-name p-name-type-2')
                item['name'] = name.text.strip()
                item['url'] = name.find('a')['href'].strip()
                item['category'] = self.category
                item['uniqueId'] = goods['data-sku']
            except:
                continue
            try:
                item['brand'] = re.findall(pattern,item['name'])[0]
            except:
                item['brand'] = '其他'
            yield item
            # print(name.text.strip(),price.text.strip(),href)


