# Generated by Django 3.1.1 on 2020-09-10 02:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20200910_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 10, 28, 52, 619100)),
        ),
        migrations.AlterField(
            model_name='device',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 10, 28, 52, 619100)),
        ),
    ]