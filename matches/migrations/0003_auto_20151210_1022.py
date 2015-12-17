# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_auto_20151210_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advocate',
            old_name='username',
            new_name='user',
        ),
        migrations.AddField(
            model_name='advocate',
            name='how_added',
            field=models.CharField(default='user add self', max_length=200),
            preserve_default=False,
        ),
    ]
