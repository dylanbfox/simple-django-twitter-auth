# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('OAUTH_TOKEN', models.CharField(max_length=199, null=True, blank=True)),
                ('OAUTH_TOKEN_SECRET', models.CharField(max_length=199, null=True, blank=True)),
                ('username', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
