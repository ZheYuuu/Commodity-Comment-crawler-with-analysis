# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:entrypoint.py
@time:2018/4/2210:47
"""

from scrapy.cmdline import execute
# execute(['scrapy','crawl','getCommodityInfo','-a','searchKey=手机','-a','category=electronics','-a','num=60'])
execute(['scrapy','crawl','getCommentDetail','-a','uniqueId=43172916757'])
# execute(['scrapy','crawl','getCommentSummary','-a','uniqueId=6157652'])
#