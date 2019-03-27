from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .models import JDCommentDetail
from .models import JDCommodity
from .models import JDCommentSummary
from scrapyd_api import ScrapydAPI
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from uuid import uuid4
import json
import time


scrapyd = ScrapydAPI('http://localhost:6800')
# Create your views here.

def index(request):
    # obj_list = JDCommodity.objects.all()
    # context = {"obj_list":obj_list}
    return render(request,'main/index.html')
# TODO: 跳转需等待，可尝试提供一个任务状态界面。
def getCommodityInfo(request):
    if request.method=="POST":
        # get POST parameters
        searchKey = request.POST.get('searchKey')
        category = request.POST.get('category')
        num = request.POST.get('num')
        print("Enter the POST view!  ", searchKey, category)

        # spider setting
        settings = {
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        # taskId to indentify each task
        task = scrapyd.schedule('JDSpider', 'getCommodityInfo',
                                settings=settings, searchKey=searchKey, category=category, num=num)
        print("It seems everything is running well? ")
        status = {'taskId': task, 'status': 'started'}
        return HttpResponseRedirect(reverse('main:commodityInfoPage',args=(category,searchKey)))

        # return HttpResponse(json.dumps(status), content_type="application/json,charset=utf-8")
        # return JsonResponse(status,safe=False)
    elif request.method=="GET":
        taskId = request.GET.get("taskId",None)
        uniqueId = request.GET.get("uniqueId",None)
        print("Enter the GET view!  ", taskId, uniqueId)
        if not taskId and not uniqueId:
            return JsonResponse({"error":"Missing args"})

        status = scrapyd.job_status("JDSpider",taskId)
        if status == "finished":
            try:
                item = JDCommodity.Objects.get(uniqueId = uniqueId)
                return JsonResponse({"data":item.to_dict})
            except Exception as e:
                return JsonResponse({"error":str(e)})
        else:
            return JsonResponse({'status': status})

def getCommodityCommentSummary(request):
    if request.method=="POST":
        uniqueId = request.POST.get("uniqueId")
        task = scrapyd.schedule('JDSpider','getCommentSummary',uniqueId=uniqueId)
        return HttpResponseRedirect(reverse('main:commodityCommentSummaryPage', args=(uniqueId,)))

def getCommodityCommentDetail(request):
    if request.method=="POST":
        uniqueId = request.POST.get("uniqueId")
        # taskId to indentify each task
        task = scrapyd.schedule('JDSpider', 'getCommentDetail',uniqueId=uniqueId)
        return HttpResponseRedirect(reverse('main:commodityCommentPage',args=(uniqueId,)))

def commodityInfoPage(request,searchKey,category):
    # 集成scrapy
    print("enter commodityInfoPage")
    commodityList = JDCommodity.objects.filter(searchKey=searchKey).all()

    paginator = Paginator(commodityList, 20)
    # page = request.POST.get('page')
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        # If page request (9999) is out of range, deliver last page of results.
    try:
        item = paginator.page(page)
    except (EmptyPage, InvalidPage):
        item = paginator.page(paginator.num_pages)

    context = {'commodityList': item}
    return render(request, 'main/commodityInfoPage.html', context)

def commodityCommentPage(request, commodityId):
    print("enter commodityCommentPage",commodityId)
    commentList = JDCommentDetail.objects.filter(commodityId=commodityId).all()

    paginator = Paginator(commentList, 20)
    # page = request.POST.get('page')
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        # If page request (9999) is out of range, deliver last page of results.
    try:
        item = paginator.page(page)
    except (EmptyPage, InvalidPage):
        item = paginator.page(paginator.num_pages)
    context = {'commentList':item}

    return render(request,'main/commodityCommentPage.html',context)

def commodityCommentSummaryPage(request,commodityId):
    commentSummary = JDCommentSummary.objects.get(commodityId=commodityId)
    name = JDCommodity.objects.get(uniqueId=commodityId).name
    hotTags = json.loads(commentSummary.hotCommentTagStatistics)
    context = {"commentSummary":commentSummary,"name":name,"hotTags":hotTags}
    return render(request,'main/commodityCommentSummaryPage.html',context)