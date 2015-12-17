# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0005_auto_20151210_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvocateChangeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('ip_of_change', models.CharField(max_length=200)),
                ('changed_date', models.DateTimeField(auto_now_add=True)),
                ('circles', models.ManyToManyField(to='matches.Circle', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'advocate_changes',
            },
        ),
        migrations.AlterField(
            model_name='advocate',
            name='how_added',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
