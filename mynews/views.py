from datetime import datetime, timedelta, time

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect

from mynews import signals
from mynews.models import News, Comments, Spot, Activities, UserProfile
from mynews.signals import comments_done


def index(request):
    return render(request, 'mynews/index.html')

def activity(request):
    activity_list = Activities.objects.all().order_by('-pub_date')
    
    return render(request, 'mynews/activity.html', {'activity_list': activity_list})

def today(request):
    
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    #오늘 News와 Spot price 받아와
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price_list = Spot.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price = spot_price_list.first()
    
    if request.method == 'POST':
        comment_text = request.POST.get("comment_text", False)
        publisher_text = request.user.username
        pub_date = datetime.now()
        news_id = request.POST.get("news_id", False)
        
        news = News.objects.get(pk = news_id)

        #signal / tag 1 = commnet
        comments_done.send(sender=None, publisher_text=publisher_text, title_text=news.title_text, pub_date=pub_date, comment_text=comment_text, tag='1')
        
        #db 객체만듬
        c = Comments(news=news, comment_text=comment_text, publisher_text=publisher_text, pub_date=pub_date)
        c.save()
        
        #comment_list = Comments.objects.filter(news=news)
        #print(comment_list) 
        
        #return render(request, 'mynews/detail.html', {'news': news, 'comment_list':comment_list})
        
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
    
    #Comment를 Post 했을 경우
    if request.method == 'POST':
        comment_text = request.POST.get("comment_text", False)
        publisher_text = request.user.username
        pub_date = datetime.now()
        
        #signal / tag 1 = commnet
        comments_done.send(sender=None, publisher_text=publisher_text, title_text=news.title_text, pub_date=pub_date, comment_text=comment_text, tag='1')
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

def comment_delete(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    print(comment)
    comment.delete()
    
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    #오늘 News와 Spot price 받아와
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price_list = Spot.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price = spot_price_list.first()
    
        
    #Comments모델 객체 받아와 ( 오늘 News의 Comments들만)
    comment_list = Comments.objects.filter(news=daily_news_list)
    comment_list_count = comment_list.count()
    
    return render(request, 'mynews/today.html', {'daily_news_list': daily_news_list, 'spot_price': spot_price, 'comment_list': comment_list, 'comment_list_count': comment_list_count} )
    

def comment_edit(request):
    return

