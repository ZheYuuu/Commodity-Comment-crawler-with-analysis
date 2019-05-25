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
        self.rootUrl = "https://item.jd.com/" + self.uniqueId + ".html"
        self.start_urls = [self.rootUrl]
        self.headers = {
            "Referer": self.rootUrl,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

    # def start_requests(self):
    #     self.headers = {
    #         "Referer": self.rootUrl,
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    #     }
    #     yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        maxNum = 30
        # yield Request('http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv74&' \
        #               'productId=%s&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page=0'%(self.uniqueId), headers = self.headers, callback=self.getCommentDetail)

        for j in range(1,4):
            bashUrl = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4985&' \
                       'productId=%s&score=%s&sortType=5&pageSize=10&isShadowSku=0&fold=1&page=' %(self.uniqueId, str(j))
            for i in range(maxNum):
                url = bashUrl + str(i)

                yield Request(url, headers = self.headers, callback=self.getCommentDetail)

    def getCommentDetail(self,response):
        try:
            j = self.transferToJson(response)
        except:
            print("Error!!! This url returns: ",response.text)
            return
        comments = j['comments']
        print(comments)
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
        try:
            res = re.match("^fetchJSON_comment(\w+)\((.*?)\);", response.text).groups()[1]
            return json.loads(res)
        except:
            print("response text:", response.text)
            raise Exception("Fail to transfer response.text to json in commentSummary!")


