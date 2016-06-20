# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 10:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EtcdCluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('cluster_endpoint', models.CharField(max_length=300)),
                ('cluster_prefix', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('0', 'READY'), ('1', 'UP'), ('2', 'DOWN'), ('3', 'UNKOWN')], default=0, max_length=1)),
                ('version', models.CharField(default='UNKOWN', max_length=50)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'etcdcluster',
                'db_table': 'etcdcluster',
            },
        ),
        migrations.AlterUniqueTogether(
            name='etcdcluster',
            unique_together=set([('cluster_endpoint',)]),
        ),
    ]