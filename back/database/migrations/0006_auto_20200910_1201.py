# Generated by Django 3.1.1 on 2020-09-10 04:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20200910_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 12, 1, 6, 701251)),
        ),
        migrations.AlterField(
            model_name='device',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 12, 1, 6, 701251)),
        ),
    ]
