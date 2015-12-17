# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0003_auto_20151210_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleChangeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('changed_date', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
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
            ],
            options={
                'verbose_name_plural': 'single_changes',
            },
        ),
        migrations.RemoveField(
            model_name='single_change_log',
            name='changed_by',
        ),
        migrations.RemoveField(
            model_name='single_change_log',
            name='single',
        ),
        migrations.RenameField(
            model_name='single',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='single',
            old_name='lastname',
            new_name='last_name',
        ),
        migrations.DeleteModel(
            name='Single_Change_Log',
        ),
        migrations.AddField(
            model_name='singlechangelog',
            name='single',
            field=models.ForeignKey(to='matches.Single'),
        ),
    ]
