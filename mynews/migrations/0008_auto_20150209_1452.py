# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynews', '0007_auto_20150209_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='opinion_text',
            field=models.CharField(blank=True, max_length=400),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='summary_text',
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
