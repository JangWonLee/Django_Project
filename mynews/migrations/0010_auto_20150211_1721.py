# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mynews', '0009_auto_20150211_1642'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyNews',
            new_name='Clippings',
        ),
    ]
