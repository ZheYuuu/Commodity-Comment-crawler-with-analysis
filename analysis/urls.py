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
    path("",views.analysis,name="analysis"),
    path("commentProcess/",views.commentProcess, name = "commentProcess"),

]