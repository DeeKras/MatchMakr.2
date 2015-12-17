# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advocate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('circles', models.CommaSeparatedIntegerField(max_length=150)),
                ('username', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'advocates',
            },
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=6)),
                ('admin', models.CharField(max_length=6)),
                ('admin_phone', models.CharField(max_length=15)),
                ('admin_email', models.EmailField(max_length=254)),
                ('short_desc', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=1500)),
                ('members', models.CommaSeparatedIntegerField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'circles',
            },
        ),
        migrations.CreateModel(
            name='Single',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('age', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('short_desc', models.CharField(max_length=1500)),
                ('how_advocate_knows', models.CharField(max_length=100)),
                ('mother', models.CharField(max_length=100)),
                ('father', models.CharField(max_length=100)),
                ('parents_location', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('prefered_matchmaker', models.CharField(max_length=100)),
                ('photo', models.ImageField(default=b'photos/None/no-img.jpg', upload_to=b'photos/')),
                ('profile_image', models.ImageField(default=b'profile_jpgs/None/no-img.jpg', upload_to=b'profile_jpgs/')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'singles',
            },
        ),
        migrations.CreateModel(
            name='Single_Change_Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('changed_date', models.DateTimeField(auto_now_add=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('age', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('short_desc', models.CharField(max_length=1500)),
                ('how_advocate_knows', models.CharField(max_length=100)),
                ('mother', models.CharField(max_length=100)),
                ('father', models.CharField(max_length=100)),
                ('parents_location', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('prefered_matchmaker', models.CharField(max_length=100)),
                ('photo', models.ImageField(default=b'photos/None/no-img.jpg', upload_to=b'photos/')),
                ('profile_image', models.ImageField(default=b'profile_jpgs/None/no-img.jpg', upload_to=b'profile_jpgs/')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('single', models.ForeignKey(to='matches.Single')),
            ],
            options={
                'verbose_name_plural': 'single_changes',
            },
        ),
    ]
