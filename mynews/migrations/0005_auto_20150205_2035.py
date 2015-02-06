# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynews', '0004_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='comment_text',
            field=models.CharField(max_length=400, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activities',
            name='tag',
            field=models.CharField(max_length=100, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_text',
            field=models.CharField(max_length=400),
            preserve_default=True,
        ),
    ]
