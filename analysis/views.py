from django.shortcuts import render
from main.models import JDCommentDetail
# Create your views here.

def emotionalTendencyAnalysis(request,*args,**kwargs):
    commodityId = kwargs.get("commodityId")
    data = JDCommentDetail.objects.filter(commodityId=commodityId).all()

