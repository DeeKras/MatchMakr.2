# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_auto_20151215_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='single',
            name='resume',
            field=models.FileField(default=b'resume/None/no-file.pdf', upload_to=b'resumes/'),
        ),
    ]
