# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JDCommodityItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    searchKey = scrapy.Field()
    category = scrapy.Field()
    uniqueId = scrapy.Field()

class JDCommentDetailItem(scrapy.Item):
    commodityId = scrapy.Field()
    # 评论内容
    content = scrapy.Field()
    # 评论所含图片数量
    picNum = scrapy.Field()
    # 评论所含视频数量
    videoNum = scrapy.Field()
    # 评论的回复数
    replyNum = scrapy.Field()
    # 评论是否被置顶
    isTop = scrapy.Field()
    # 评论发布时间
    creationTime = scrapy.Field()
    # 评论用户的等级
    userLevelName = scrapy.Field()
    # 用户评分[0-5]
    score = scrapy.Field()
    # 评论被点赞次数
    usefulVoteCount = scrapy.Field()

class JDCommentSummaryItem(scrapy.Item):
    # 该评论汇总所对应的商品id
    commodityId = scrapy.Field()
    # 热门的评论标签（以json string的形式存储）
    hotCommentTagStatistics = scrapy.Field()
    # 好评率
    goodRate = scrapy.Field()
    # 评论总数
    commentCountStr = scrapy.Field()
    # 差评数
    poorCountStr = scrapy.Field()
    # 中评数
    generalCountStr = scrapy.Field()
    # 好评数
    goodCountStr = scrapy.Field()
    # 视频晒单数
    videoCountStr = scrapy.Field()
    # 追评数
    afterCountStr = scrapy.Field()
    # 晒图数
    imageListCount = scrapy.Field()


