# Generated by Django 3.1.1 on 2020-09-09 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200909_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=64)),
                ('reason', models.TextField(default=None, max_length=2000)),
                ('state', models.CharField(default=None, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ShelfOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField(default=0)),
                ('owner_name', models.CharField(default=None, max_length=64)),
                ('reason', models.TextField(default=None, max_length=2000)),
                ('state', models.CharField(default=None, max_length=64)),
                ('start_time', models.DateTimeField(default=None, max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='device',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 0, 24, 23, 486430)),
        ),
        migrations.AlterField(
            model_name='device',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 0, 24, 23, 486430)),
        ),
    ]