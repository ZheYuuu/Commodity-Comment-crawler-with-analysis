# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
from JDSpider.items import JDCommodityItem,JDCommentDetailItem,JDCommentSummaryItem
from scrapy import log
class JdspiderPipeline(object):

    def __init__(self):

        self.SETTINGS = get_project_settings()
        # print("-"*100)
        # print(self.SETTINGS.attributes)
        # print("-" * 100)
        self.dbpool = adbapi.ConnectionPool('pymysql',
                                            user=self.SETTINGS['MYSQL_USER'],
                                            password=self.SETTINGS['MYSQL_PASSWD'],
                                            host=self.SETTINGS['MYSQL_HOST'],
                                            database=self.SETTINGS['MYSQL_DB'],
                                            charset='utf8',
                                            )

    def close_spider(self,spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        if isinstance(item, JDCommodityItem):
            query = self.dbpool.runInteraction(self._insert_record_basic, item)
            # query.addCallback(self._handle_error)
        if isinstance(item, JDCommentDetailItem):
            query = self.dbpool.runInteraction(self._insert_record_comment, item)
            # query.addCallback(self._handle_error)
        if isinstance(item, JDCommentSummaryItem):
            query = self.dbpool.runInteraction(self._insert_record_commentSummary, item)
        return item

    def _insert_record_basic(self,txn,item):

        name = item['name']
        price = float(item['price'])
        brand = item['brand']
        url = item['url']
        category = item['category']
        searchKey = item['searchKey']
        uniqueId = item['uniqueId']



        sql_insert = '''insert into jd_commodity(name,price,brand,url,category,searchKey,uniqueId)
                                    values('%s','%f','%s','%s','%s','%s','%s')''' \
                     % (name, price, brand, url,category, searchKey,uniqueId)
        try:
            txn.execute(sql_insert)
        except:
            print(name,"has existed!")

    def _insert_record_comment(self,txn,item):
        content = item['content']
        commodityId = item['commodityId']
        picNum = int(item['picNum'])
        videoNum = int(item['videoNum'])
        replyNum = int(item['replyNum'])
        isTop = item['isTop']
        creationTime = item['creationTime']
        userLevelName = item['userLevelName']
        score = item['score']
        usefulVoteCount = item['usefulVoteCount']

        sql_insert = '''insert into jd_comment_detail
                        (content,picNum,videoNum,replyNum,isTop,creationTime,
                        userLevelName,score,usefulVoteCount,commodityId)
                        values('%s','%d','%d','%d','%s','%s',
                        '%s','%d','%d','%s')''' \
                     % (content,picNum,videoNum,replyNum,isTop,creationTime,userLevelName,score,usefulVoteCount, commodityId)
        try:
            txn.execute(sql_insert)
        except:
            raise Exception("When inserting comment into DB, error occurred.")

    def _insert_record_commentSummary(self,txn,item):
        commodityId = item['commodityId']
        hotCommentTagStatistics = item['hotCommentTagStatistics']
        goodRate = item['goodRate']
        commentCountStr = item['commentCountStr']
        poorCountStr = item['poorCountStr']
        generalCountStr = item['generalCountStr']
        goodCountStr = item['goodCountStr']
        videoCountStr = item['videoCountStr']
        afterCountStr = item['afterCountStr']
        imageListCount = item['imageListCount']

        sql_insert = '''insert into jd_comment_summary
                        (commodityId, hotCommentTagStatistics, goodRate,
                        commentCountStr,poorCountStr,generalCountStr,goodCountStr,
                        videoCountStr,afterCountStr,imageListCount)
                        values
                        ('%s','%s','%f',
                        '%s','%s','%s','%s',
                        '%s','%s','%d')'''\
                        %(commodityId,hotCommentTagStatistics,goodRate,
                          commentCountStr,poorCountStr,generalCountStr,goodCountStr,
                          videoCountStr,afterCountStr,imageListCount)
        try:
            txn.execute(sql_insert)
        except:
            raise Exception('When inserting commentSummary into DB, error occurred.')


    def _handle_error(self,e):
        log.err(e)
