# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynews', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='opinion_text',
            field=models.CharField(default='', max_length=400),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='summary_text',
            field=models.CharField(default='', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='picture/profile-no-img.jpg', upload_to='picture/'),
            preserve_default=True,
        ),
    ]
