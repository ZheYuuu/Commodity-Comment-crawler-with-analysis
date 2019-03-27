# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:getCommentDetail.py
@time:2019/3/2417:33
"""

import scrapy
import re
from scrapy.http import Request
from JDSpider.items import JDCommentDetailItem
import json
import datetime
class GetCommentDetail(scrapy.Spider):
    name = "getCommentDetail"
    def __init__(self,*args,**kwargs):
        self.uniqueId = kwargs.get("uniqueId")
        self.bashUrl = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv74&' \
                        'productId=%s&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page='%self.uniqueId
        self.start_urls = [self.bashUrl+'1']

    def start_requests(self):
        url = self.bashUrl + '1'
        yield Request(url,callback=self.parse)

    def parse(self, response):
        maxNum = 30
        j = self.transferToJson(response)
        hotComments = j['hotCommentTagStatistics']
        # storing hot comments remains unfinished

        for i in range(maxNum):
            url = self.bashUrl + str(i)
            yield Request(url, callback=self.getCommentDetail)

    def getCommentDetail(self,response):
        j = self.transferToJson(response)
        comments = j['comments']
        for comment in comments:
            item = JDCommentDetailItem()
            item["commodityId"] = self.uniqueId
            item["content"] = comment['content']
            item['picNum'] = len(comment['images']) if 'images' in comment else 0
            item['videoNum'] = len(comment['videos']) if 'videos' in comment else 0
            item['replyNum'] = comment['replyCount']
            item['isTop'] = 1 if comment['isTop'] else 0
            item['creationTime'] = comment['creationTime']
            # item['creationTime'] = datetime.datetime.strptime(comment['creationTime'],'%Y-%m-%d %H:%M:%S')
            item['userLevelName'] = comment['userLevelName']
            item['score'] = comment['score']
            item['usefulVoteCount'] = int(comment['usefulVoteCount']) - int(comment['uselessVoteCount'])
            yield item

    def transferToJson(self,response):
        fetch_pattern = 'fetchJSON_comment\w+\((.*?)\);'
        pattern = re.compile(fetch_pattern)
        try:
            t = re.search(pattern, response.text).group(1)
        except:
            return Exception
        j = json.loads(t)
        return j

