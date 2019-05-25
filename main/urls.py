# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:urls.py
@time:2019/3/1418:05
"""

from django.urls import path
from . import views

# 在一个真实的 Django 项目中，可能会有五个，十个，二十个，甚至更多应用。Django 如何分辨重名的 URL 呢？
# 举个例子，main 应用有 index 视图，可能另一个应用也有同名的视图。
# Django 如何知道 {% url %} 标签到底对应哪一个应用的 URL 呢？
# 答案是：在根 URLconf 中添加命名空间。在 main/urls.py 文件中稍作修改，加上 app_name 设置命名空间,
# 并编辑对应的模板html：{% url 'index' %}">   ------->   {% url 'main:index' %}
app_name = 'main'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('getCommodityInfo/',views.getCommodityInfo, name = 'getCommodityInfo'),
    path('getCommodityCommentDetail/',views.getCommodityCommentDetail, name="getCommodityCommentDetail"),
    path('getCommodityCommentSummary/',views.getCommodityCommentSummary, name="getCommodityCommentSummary"),
    path('getTaskStatus/',views.getTaskStatus, name = 'getTaskStatus'),
    path('commodityInfo/<str:category>/<str:searchKey>/',views.commodityInfoPage, name = 'commodityInfoPage'),
    path('commentsInfo/<str:commodityId>/',views.commodityCommentPage,name = 'commodityCommentPage'),
    path('commentSummary/<str:commodityId>/',views.commodityCommentSummaryPage,name = 'commodityCommentSummaryPage'),
]
