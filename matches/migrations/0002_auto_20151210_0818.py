# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='admin',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='circle',
            name='desc',
            field=models.CharField(max_length=1500, blank=True),
        ),
        migrations.AlterField(
            model_name='circle',
            name='members',
            field=models.CommaSeparatedIntegerField(max_length=150, blank=True),
        ),
    ]
