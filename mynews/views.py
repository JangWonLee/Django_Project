#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
import json

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query_utils import Q
from django.dispatch import Signal
from django.http import response
from django.http.request import QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt

from mynews import signals
from mynews.models import News, Comments, Spot, Activities, Clippings
from mynews.signals import comments_done


def index(request):
    return render(request, 'mynews/index.html')


@csrf_exempt
def activity(request):
    print("acitivy call")
    activity_list = Activities.objects.all().order_by('-pub_date')
    
    activity_list_dict = []
    if request.method == 'POST':
        for activity in activity_list:
            activity_list_dict.append(as_dict_activity(activity))
            
        json_obj = json.dumps({"activity_list": activity_list_dict})
        print(json_obj)
        print("activity request call")
        return HttpResponse(json_obj, content_type="application/json")
    
    else:    
        paginator = Paginator(activity_list, 10)
        page = request.GET.get('page')
        try:
            activity_list = paginator.page(page)
        except PageNotAnInteger:
            activity_list = paginator.page(1)
        except EmptyPage:
            activity_list = paginator.page(paginator.num_pages)
        
        print("activity render call")
        return render(request, 'mynews/activity.html', {'activity_list': activity_list})

def clipping(request):
    clipping_list = request.user.clippings.all().order_by('-pub_date')
    
    #Pagination
    paginator = Paginator(clipping_list, 10)
    page = request.GET.get('page')
    try:
        clipping_list = paginator.page(page)
    except PageNotAnInteger:
        clipping_list = paginator.page(1)
    except EmptyPage:
        clipping_list = paginator.page(paginator.num_pages)
    
    return render(request, 'mynews/clipping.html', {'clipping_list': clipping_list})

def today(request):
    print("today call")
    
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    #오늘 News와 Spot price 받아와
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start).order_by('-pub_date')
    spot_price_list = Spot.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price = spot_price_list.first()
    
    for news in daily_news_list:
        news.is_clipped_by_me = request.user.clippings.filter(news=news).exists()
    
    ##@##
    #Comments모델 객체 받아와 ( 오늘 News의 Comments들만)
    comment_list = Comments.objects.filter(news=daily_news_list)
    comment_list_count = comment_list.count()
    
    #context = {}
    return render(request, 'mynews/today.html', {'daily_news_list': daily_news_list, 'spot_price': spot_price, 'comment_list': comment_list, 'comment_list_count': comment_list_count} )


def archive(request):
    #모든 News 받아와
    archive_news_list = News.objects.order_by('-pub_date')[:]

    #Pagination
    paginator = Paginator(archive_news_list, 10)
    page = request.GET.get('page')
    try:
        archive_news = paginator.page(page)
    except PageNotAnInteger:
        archive_news = paginator.page(1)
    except EmptyPage:
        archive_news = paginator.page(paginator.num_pages)
    
    return render(request, 'mynews/archive.html', {"archive_news": archive_news})

def as_dict_activity(activity):
    return {
            "publisher_text": activity.publisher_text,
            "title_text": activity.title_text,
            "comment_text": activity.comment_text,
            "pub_date": activity.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "tag": activity.tag
    }

def as_dict_comment(comment):
    return {
            "publisher_text": comment.publisher_text,
            "comment_id": comment.id,
            "news_id": comment.news_id,
            "pub_date": comment.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
           "comment_text": comment.comment_text
    }
    
def as_dict_news(news):
    return {
            "news_id": news.id,
            "opinion_text": news.opinion_text,
            "link_text": news.link_text,
            "is_clipped_by_me": news.is_clipped_by_me,
            "summary_text": news.summary_text,
            "title_text": news.title_text,
            "pub_date": news.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
    }    

@csrf_exempt
def detail(request, news_id):
    #news_id를 갖는 News 불러와
    news = get_object_or_404(News, pk=news_id)
    
    news.is_clipped_by_me = request.user.clippings.filter(news=news).exists()
    
    comment_list = Comments.objects.filter(news=news)
    comment_list_count = comment_list.count()
    
    print(comment_list)
    
    if request.method == 'POST':
        print("request")
        
        comment_list_dict = []
        for comment in comment_list:
            comment_list_dict.append(as_dict_comment(comment))
            
        news_dict = []
        news_dict = as_dict_news(news)
        
        json_obj = json.dumps({"news": news_dict, "comment_list_count": comment_list_count, "comment_list": comment_list_dict })
        
        print("detail request call")
        return HttpResponse(json_obj, content_type="application/json")
    else:
        print("detail render call")
        return render(request, 'mynews/detail.html', {'news': news, 'comment_list':comment_list, 'comment_list_count': comment_list_count})
    


def login_view(request):
    print("login_view call")
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if user.is_active:
                login(request, user)
                
                activity_list = Activities.objects.all().order_by('-pub_date')
                return render(request, 'mynews/activity.html', {'activity_list': activity_list})

            else:
                print(22)
        else:
            print(33)
            message = "No"
            context = {'message': message}
            return render(request, 'mynews/login.html', context)
    else:
        print(22222222)
        return render(request, 'mynews/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'mynews/logout.html')

@csrf_exempt
def comment_post(request):
    print("comment_post call")
    
    if request.method == 'POST':
        
        data = json.loads(request.body.decode("utf-8"))
        
        news_id = data.get('news_id')
        comment_text = data.get('comment_text')
        
        publisher_text = request.user.username
        pub_date = datetime.now()
        
        news = News.objects.get(pk=news_id)
        
        #signal / tag 1 = post
        comments_done.send(sender=None, publisher_text=publisher_text, title_text=news.title_text, pub_date=pub_date, comment_text=comment_text, tag='1')
        
        c = Comments(news=news, comment_text=comment_text, publisher_text=publisher_text, pub_date=pub_date)
        c.save()
        
        comment = Comments.objects.all().last()
        comment_id = comment.id
        
        
        json_obj = json.dumps({"news_id": news_id, "publisher_text": publisher_text, "comment_text":comment_text, "comment_id": comment_id, "pub_date": pub_date.strftime("%Y-%m-%d %H:%M:%S")})
        print(json_obj)
        return HttpResponse(json_obj, content_type="application/json")
    else:
        return HttpResponse("comment_post fail")

@csrf_exempt
def comment_delete(request):
    print("comment_delete call")
    
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        
        news_id = data.get('news_id', False)
        comment_id = data.get('comment_id')
        
        news = News.objects.get(pk=news_id)
        comment = Comments.objects.get(pk=comment_id)
        
        #signal/ tag3 = delete
        comments_done.send(sender=None, publisher_text=request.user.username, title_text=news.title_text, pub_date=datetime.now(), comment_text=comment.comment_text, tag='3')
        comment.delete()
        
        json_obj = json.dumps({"comment_id": comment_id})
        
        return HttpResponse(json_obj, content_type="application/json")
    else:
        return HttpResponse("comment_delete fail")
    
    
    ##
    
@csrf_exempt
def comment_edit(request):
    print("comment_edit call")
    
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        news_id = data.get('news_id', False)
        comment_id = data.get('comment_id', False)
        edit_comment_text = data.get('edit_text', False)
        
        news = News.objects.get(pk=news_id)

        print(request.user.id)
        
        #signal/ tag2 = edit
        comments_done.send(sender=None, publisher_text=request.user.username, title_text=news.title_text, pub_date=datetime.now(), comment_text=edit_comment_text, tag='2')
        
        
        comment = Comments.objects.get(pk=comment_id)
        comment.comment_text = edit_comment_text
        comment.pub_date = datetime.now()
        
        comment.save()
        return HttpResponse(edit_comment_text);
    else:
        return HttpResponse("Something Wrong")
    
@csrf_exempt
def news_clip(request):
    print("news_clip call")
    
    if request.method == 'POST':
        
        user = request.user
        pub_date = datetime.now()
        
        data = json.loads(request.body.decode("utf-8"))
        news_id = data.get('news_id')
        
        news = News.objects.get(pk=news_id)
        
        c = Clippings(user=user, news=news, pub_date=pub_date)
        c.save()
                
        return HttpResponse("news_clip Success")
    else:
        return HttpResponse("news_clip Fail")
    
@csrf_exempt
def news_clip_cancel(request):
    print("news_clip_cancel call")
    
    if request.method == 'POST':
        
        user = request.user
        
        data = json.loads(request.body.decode("utf-8"))
        news_id = data.get('news_id')
        news = News.objects.get(pk=news_id)
        
        c = Clippings.objects.filter(news=news, user=user)
        c.delete()
                
        return HttpResponse("news_clip_cancel Success")
    else:
        return HttpResponse("news_clip_cancel Fail")
    
def news_search(request):
    print("news_search call")
    if request.method == 'POST':
        search_text = request.POST.get('search-text', False)
        search_news_list = News.objects.filter(title_text__contains=search_text).order_by('-pub_date')
        
        #Pagination
        paginator = Paginator(search_news_list, 10)
        page = request.GET.get('page')
        try:
            archive_news = paginator.page(page)
        except PageNotAnInteger:
            archive_news = paginator.page(1)
        except EmptyPage:
            archive_news = paginator.page(paginator.num_pages)
        
        return render(request, 'mynews/archive.html', {'archive_news': archive_news})
    else:
        return HttpResponse("fail")

def test(request):
    
    return render(request, 'mynews/test.html')
