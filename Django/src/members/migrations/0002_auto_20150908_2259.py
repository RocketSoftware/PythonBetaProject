# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersAdmin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('member_id', models.CharField(max_length=100)),
                ('member_first_name', models.CharField(blank=True, null=True, max_length=100)),
                ('member_last_name', models.CharField(blank=True, null=True, max_length=100)),
                ('member_address', models.CharField(blank=True, null=True, max_length=100)),
                ('member_city', models.CharField(blank=True, null=True, max_length=100)),
                ('member_state_code', models.CharField(blank=True, null=True, max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Members',
        ),
    ]
