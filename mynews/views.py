from datetime import datetime, timedelta, time

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect

from mynews.models import News, Comments, Spot, Activities
from mynews import signals
from mynews.signals import comments_done


def index(request):
    print("index call")
    
    activity_list = Activities.objects.all().order_by('-pub_date')
    
    return render(request, 'mynews/index.html', {'activity_list': activity_list})

def today(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price_list = Spot.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price = spot_price_list.first()
    context = {'daily_news_list': daily_news_list, 'spot_price': spot_price }
    return render(request, 'mynews/today.html', context)

def detail(request, news_id):
    print("detail call")
    if request.method == 'POST':
        news = get_object_or_404(News, pk=news_id)
        comment_text = request.POST.get("comment_text", False)
        publisher_text = request.user.username
        pub_date = datetime.now()
        
        #signal / tag 1 = commnet
        comments_done.send(sender=None, publisher_text=publisher_text, title_text=news.title_text, pub_date=pub_date, comment_text=comment_text, tag='1')
        #db 객체만듬
        c = Comments(news=news, comment_text=comment_text, publisher_text=publisher_text, pub_date=pub_date)
        c.save()
        
        comment_list = Comments.objects.filter(news=news)
        print(comment_list) 
        
        return render(request, 'mynews/detail.html', {'news': news, 'comment_list':comment_list})
    else:
        news = get_object_or_404(News, pk=news_id)
        comment_list = Comments.objects.filter(news=news)
        print(comment_list) 
        return render(request, 'mynews/detail.html', {'news': news, 'comment_list':comment_list})
    

def prev(request):
    previous_news_list = News.objects.order_by('-pub_date')[:]
    # context질문, return 방법
#    context = {'previous_news_list': previous_news_list}
    
    paginator = Paginator(previous_news_list, 10)
    # 질문
    page = request.GET.get('page')
    
    try:
        previous_news = paginator.page(page)
    except PageNotAnInteger:
        previous_news = paginator.page(1)
    except EmptyPage:
        previous_news = paginator.page(paginator.num_pages)
    
    return render(request, 'mynews/prev.html', {"previous_news": previous_news})

def login_view(request):
    print(111111111)
    if request.method == 'POST':
        print(22222222)
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None and user.is_active:
            if user.is_active:
                login(request, user)
                print(11)
                return redirect('/mynews')     
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
    


