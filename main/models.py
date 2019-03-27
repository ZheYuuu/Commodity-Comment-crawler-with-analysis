from django.db import models
import json
# Create your models here.
class JDCommodity(models.Model):
    class Meta:
        db_table = "jd_commodity"
    # 商品名称
    name = models.CharField(max_length=255)
    # 商品价格
    price = models.FloatField()
    # 商品品牌
    brand = models.CharField(max_length=255)
    # 商品对应链接
    url = models.CharField(max_length=255)
    # 搜索关键词
    searchKey = models.CharField(max_length=255)
    # 商品所属品类
    category = models.CharField(max_length=255)
    # 商品的唯一表示id
    uniqueId = models.CharField(max_length=255,unique=True)

    @property
    def to_dict(self):
        data = {
            'name': self.name,
            'price': self.price,
            'brand':self.brand,
            'url':self.url,
            'searchKey':self.searchKey,
            'category':self.category,
            'uniqueId':self.uniqueId,
        }
        return data

    def __str__(self):
        return self.name

class JDCommentDetail(models.Model):
    class Meta:
        db_table = "jd_comment_detail"
    # 评论所对应的商品id
    commodityId = models.CharField(max_length=255)
    # 评论内容
    content = models.TextField()
    # 评论所含图片数量
    picNum = models.IntegerField()
    # 评论所含视频数量
    videoNum = models.IntegerField()
    # 评论的回复数
    replyNum = models.IntegerField()
    # 评论是否被置顶
    isTop = models.IntegerField()
    # 评论发布时间
    creationTime = models.DateTimeField()
    # "2019-02-01 09:31:53"
    # 评论用户的等级
    userLevelName = models.CharField(max_length=50)
    # 用户评分[0-5]
    score = models.IntegerField()
    # 评论被点赞次数
    usefulVoteCount = models.IntegerField()

    def __str__(self):
        return self.content

class JDCommentSummary(models.Model):
    class Meta:
        db_table = "jd_comment_summary"
    # 该评论汇总所对应的商品id
    commodityId = models.CharField(max_length=255,unique=True)
    # 热门的评论标签（以json string的形式存储）
    hotCommentTagStatistics = models.TextField()
    # 好评率
    goodRate = models.FloatField()
    # 评论总数
    commentCountStr = models.CharField(max_length=255)
    # 差评数
    poorCountStr = models.CharField(max_length=255)
    # 中评数
    generalCountStr = models.CharField(max_length=255)
    # 好评数
    goodCountStr = models.CharField(max_length=255)
    # 视频晒单数
    videoCountStr = models.CharField(max_length=255)
    # 追评数
    afterCountStr = models.CharField(max_length=255)
    # 晒图数
    imageListCount = models.IntegerField()




