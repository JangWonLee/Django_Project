# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynews', '0008_auto_20150209_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyNews',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=100)),
                ('news_id', models.IntegerField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AlterField(
            model_name='comments',
            name='news',
            field=models.ForeignKey(related_name='comments', to='mynews.News'),
            preserve_default=True,
        ),
    ]
