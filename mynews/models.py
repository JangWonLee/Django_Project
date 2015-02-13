import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from distutils.command.upload import upload


class News(models.Model):
    title_text = models.CharField(max_length=200)
    link_text = models.CharField(max_length=200)
    summary_text = models.CharField(max_length=200, blank=True)
    opinion_text = models.CharField(max_length=400, blank=True)
    pub_date = models.DateTimeField('date published')
    def __str__(self):              # __unicode__ on Python 2
        return self.title_text
        return self.link_text
        return self.summary_text
        return self.opinion_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    @property 
    def comment_count(self):
        return self.comments.all().count()

class Comments(models.Model):
    news = models.ForeignKey(News, related_name='comments')
    comment_text = models.CharField(max_length=400)
    publisher_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.comment_text
        return self.publisher_text

class Spot(models.Model):
    henryhub_text = models.CharField(max_length=200)
    wticushing_text = models.CharField(max_length=200)
    closedday_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.henryhub_text
        return self.wticushing_text
        return self.closedday_text

class Activities(models.Model):
    publisher_text = models.CharField(max_length=200) 
    title_text = models.CharField(max_length=200)
    comment_text = models.CharField(max_length=400, default='')
    pub_date = models.DateTimeField('date published')
    tag = models.CharField(max_length=100, default='')
    def __str__(self):
        return self.publisher_text
        return self.title_text
        return self.comment_text
        return self.tag

class Clippings(models.Model):
    #user_id = models.IntegerField(max_length=100)
    user = models.ForeignKey(User, related_name='clippings')
    news = models.ForeignKey(News, related_name='clippings')
    #news_id = models.IntegerField(max_length=100)
    pub_date = models.DateTimeField('date published')
    
    