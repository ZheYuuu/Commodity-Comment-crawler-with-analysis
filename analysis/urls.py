# -*- coding:utf-8 -*-
"""
@author:ZheYu
@file:urls.py.py
@time:2019/3/2713:02
"""
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path("emotionalTendencyAnalysis/<str:commodityId>/",views.emotionalTendencyAnalysis,name="emotionalTendencyAnalysis"),
]