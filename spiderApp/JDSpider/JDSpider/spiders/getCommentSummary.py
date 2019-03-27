# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:getCommentSummary.py
@time:2019/3/2612:56
"""
import scrapy
from scrapy.http import Request
import json
import re
from JDSpider.items import JDCommentSummaryItem
class GetCommentSummary(scrapy.Spider):
    name = 'getCommentSummary'
    def __init__(self,*args,**kwargs):
        self.uniqueId = kwargs.get("uniqueId")
        self.bashUrl = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv74&' \
                       'productId=%s&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page=' % self.uniqueId
        self.start_urls = [self.bashUrl + "1"]
        # testUrl = 'sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv74&productId=1186228&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page=1'

    # def start_requests(self):
    #     url = [self.bashUrl + "1"]
    #     yield Request(url,callback=self.parse)

    def parse(self, response):
        j = self.transferToJson(response)
        item = JDCommentSummaryItem()
        try:
            item["imageListCount"] = j["imageListCount"]
            item['commodityId'] = self.uniqueId
            hotCommentTags = j['hotCommentTagStatistics']
            d = []
            for tag in hotCommentTags:
                d.append({"name":tag['name'],'count':tag['count']})
            item['hotCommentTagStatistics'] = json.dumps(d,ensure_ascii=False)
            productCommentSummary = j['productCommentSummary']
            item['goodRate'] = productCommentSummary['goodRate']
            item['commentCountStr'] = productCommentSummary['commentCountStr']
            item['poorCountStr'] = productCommentSummary['poorCountStr']
            item['generalCountStr'] = productCommentSummary['generalCountStr']
            item['goodCountStr'] = productCommentSummary['goodCountStr']
            item['videoCountStr'] = productCommentSummary['videoCountStr']
            item['afterCountStr'] = productCommentSummary['afterCountStr']
            yield item
        except:
            return Exception("Fail to set JDCommentSummaryItem!")


    def transferToJson(self, responese):
        # fetch_pattern = 'fetchJSON_comment\w+\((.*?)\);'
        # pattern = re.compile(fetch_pattern)
        try:
            res = re.match("^fetchJSON_comment(\w+)\((.*?)\);", responese.text).groups()[1]
            return json.loads(res)
        except:
            raise Exception("Fail to transfer response.text to json in commentSummary!")


