# Generated by Django 3.1.1 on 2020-09-10 11:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20200910_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentingorder',
            name='rent_end',
            field=models.DateTimeField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='rentingorder',
            name='rent_start',
            field=models.DateTimeField(default=None, max_length=64),
        ),
        migrations.AddField(
            model_name='rentingorder',
            name='rent_state',
            field=models.CharField(default='0', max_length=64),
        ),
        migrations.AlterField(
            model_name='device',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 19, 33, 6, 403425)),
        ),
        migrations.AlterField(
            model_name='device',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 19, 33, 6, 403425)),
        ),
    ]