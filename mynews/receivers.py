from django.dispatch import receiver
from django.shortcuts import render, render_to_response

from mynews.models import Activities
from mynews.signals import comments_done


@receiver(comments_done)
def comments_receiver(sender, **kwargs):
    print("receiver call")
    publisher_text = kwargs['publisher_text']
    title_text = kwargs['title_text']
    pub_date = kwargs['pub_date']
    comment_text = kwargs['comment_text']
    tag = kwargs['tag']
    
    a = Activities(publisher_text=publisher_text, title_text=title_text, pub_date=pub_date, comment_text=comment_text, tag=tag)
    a.save()
    
    activity_list = Activities.objects.all().order_by('-pub_date')
    
    return render_to_response('mynews/index.html',{'activity_list': activity_list})
    #return render_to_response('mynews/index.html', {'publisher_text': publisher_text, 'title_text': title_text, 'pub_date': pub_date} )