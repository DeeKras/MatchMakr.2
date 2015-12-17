# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0004_auto_20151210_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advocate',
            name='circles',
        ),
        migrations.AddField(
            model_name='advocate',
            name='circles',
            field=models.ManyToManyField(to='matches.Circle', blank=True),
        ),
        migrations.RemoveField(
            model_name='circle',
            name='members',
        ),
        migrations.AddField(
            model_name='circle',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
