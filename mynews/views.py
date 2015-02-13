from datetime import datetime, timedelta, time
import json

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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

def activity(request):
    activity_list = Activities.objects.all().order_by('-pub_date')
    
    return render(request, 'mynews/activity.html', {'activity_list': activity_list})

def clipping(request):
    clipping_list = request.user.clippings.all().order_by('-pub_date')
    
    return render(request, 'mynews/clipping.html', {'clipping_list': clipping_list})

def today(request):
    print("today call")
    
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    #오늘 News와 Spot price 받아와
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
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


def detail(request, news_id):
    #news_id를 갖는 News 불러와
    news = get_object_or_404(News, pk=news_id)
    
    news.is_clipped_by_me = request.user.clippings.filter(news=news).exists()
    
    #Comment를 Post 했을 경우
    if request.method == 'POST':
        #print(request.POST['text'])
        comment_text = request.POST.get("comment_text", False)
        publisher_text = request.user.username
        pub_date = datetime.now()
        
        #signal / tag 1 = commnet
        comments_done.send(sender=None, publisher_text=publisher_text, title_text=news.title_text, pub_date=pub_date, comment_text=comment_text, tag='1')
        print("detail-signal call")
        
        #db 객체만듬
        c = Comments(news=news, comment_text=comment_text, publisher_text=publisher_text, pub_date=pub_date)
        c.save()
        
    comment_list = Comments.objects.filter(news=news)
    comment_list_count = comment_list.count()
    print(comment_list) 
    return render(request, 'mynews/detail.html', {'news': news, 'comment_list':comment_list, 'comment_list_count': comment_list_count})
    


def login_view(request):
    print(111111111)
    if request.method == 'POST':
        print(22222222)
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
        return render(request, 'mynews/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'mynews/logout.html')

@csrf_exempt
def comment_post(request):
    
    if request.method == 'POST' and request.is_ajax():
        print("comment_post call")
        news_id = request.POST.get('news_id', False)
        comment_text = request.POST['comment_text']
        
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
    
    if request.method == 'POST' and request.is_ajax():
        news_id = request.POST.get('news_id', False)
        comment_id = request.POST['comment_id']
        
        news = News.objects.get(pk=news_id)
        comment = Comments.objects.get(pk=comment_id)
        
        print(news_id)
        print(comment_id)
        print(news)
        print(comment)
        
        
        #signal/ tag3 = delete
        comments_done.send(sender=None, publisher_text=request.user.username, title_text=news.title_text, pub_date=datetime.now(), comment_text=comment.comment_text, tag='3')
        
        comment.delete()
        
        return HttpResponse("comment_delete success")
    else:
        return HttpResponse("comment_delete fail")
    
    
    ##
    
@csrf_exempt
def comment_edit(request):
    print("comment_edit call")
    
    if request.method == 'POST' and request.is_ajax():
        news_id = request.POST.get('news_id', False)
        comment_id = request.POST.get('comment_id', False)
        
        print(comment_id)
        print(request.POST['edit_comment_text'])
        print("comment->POST")
        
        edit_comment_text = request.POST['edit_comment_text']
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
    
    if request.method == 'POST' and request.is_ajax():
        print("news_clip ajax")
        
        user = request.user
        pub_date = datetime.now()
        news_id = request.POST['news_id']
        
        news = News.objects.get(pk=news_id)
        
        c = Clippings(user=user, news=news, pub_date=pub_date)
        c.save()
                
        return HttpResponse("news_clip Success")
    else:
        return HttpResponse("news_clip Fail")
    
@csrf_exempt
def news_clip_cancel(request):
    print("news_clip_cancel call")
    
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        news_id = request.POST['news_id']
        news = News.objects.get(pk=news_id)
        
        c = Clippings.objects.filter(news=news, user=user)
        c.delete()
                
        return HttpResponse("news_clip_cancel Success")
    else:
        return HttpResponse("news_clip_cancel Fail")
    

