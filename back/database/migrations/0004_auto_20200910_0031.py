# Generated by Django 3.1.1 on 2020-09-09 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20200910_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 0, 31, 48, 388770)),
        ),
        migrations.AlterField(
            model_name='device',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 10, 0, 31, 48, 388770)),
        ),
    ]