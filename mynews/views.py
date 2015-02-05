import datetime

from datetime import datetime, timedelta, time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response,\
    redirect
from django.template import RequestContext, loader
from django.utils import timezone
from django.views import generic

from mynews.models import News, Comments, Spot


def index(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    daily_news_list = News.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price_list = Spot.objects.filter(pub_date__lte=today_end, pub_date__gte=today_start)
    spot_price = spot_price_list.first()
    context = {'daily_news_list': daily_news_list, 'spot_price': spot_price }
    return render(request, 'mynews/index.html', context)

def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render(request, 'mynews/detail.html', {'news': news})

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
    


