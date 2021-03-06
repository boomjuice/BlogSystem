# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-11 02:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_auto_20180811_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlestatus',
            name='status',
            field=models.BooleanField(choices=[(1, '踩'), (0, '赞')], verbose_name='赞踩状态'),
        ),
        migrations.AlterField(
            model_name='trouble',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='trouble',
            name='evaluate',
            field=models.IntegerField(blank=True, choices=[(1, '不是很舒服'), (3, '舒服舒服'), (4, 'nice'), (2, '可还行')], default=2, null=True),
        ),
        migrations.AlterField(
            model_name='trouble',
            name='status',
            field=models.IntegerField(choices=[(2, '处理中'), (1, '未处理'), (3, '已处理')], default=1),
        ),
    ]
