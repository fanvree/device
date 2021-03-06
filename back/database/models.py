from django.db import models
import datetime

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=1000, default=None)
    email = models.CharField(max_length=64, default=None)
    contact = models.CharField(max_length=64, default=None)
    identity = models.CharField(max_length=64, default=None)    # normal owner admin
    apply = models.CharField(max_length=64, default=None)       # 用户成为提供者的
    token = models.CharField(max_length=64, default=None)


class Device(models.Model):
    device_name = models.CharField(max_length=64, default=None)
    owner = models.CharField(max_length=64, default=None)
    owner_phone = models.CharField(max_length=64, default=None)
    # user = models.CharField(max_length=64, default=None)
    # rent_out = models.CharField(default=False)
    # start = models.DateField(default=datetime.datetime.now())    # TODO
    # due = models.DateField(default=datetime.datetime.now())
    location = models.CharField(max_length=64, default=None)
    addition = models.CharField(max_length=64, default=None)
    valid = models.CharField(max_length=64, default=None)
    #off_shelf on_shelf renting on_order
    reason = models.CharField(max_length=64, default=None)


class RentingOrder(models.Model):
    device_id = models.IntegerField(default=0)
    username = models.CharField(max_length=64, default=None)
    reason = models.TextField(max_length=2000, default=None)
    contact = models.TextField(max_length=64, default=None)
    start = models.DateField(max_length=64, default=None)
    due = models.DateField(max_length=64, default=None)
    valid = models.CharField(max_length=64, default=None)
    rent_state = models.CharField(max_length=64, default='default')
    rent_start = models.DateField(max_length=64, default=None)
    rent_end = models.DateField(max_length=64, default=None)


class ShelfOrder(models.Model):
    device_id = models.IntegerField(default=0)
    owner_name = models.CharField(max_length=64, default=None)
    reason = models.TextField(max_length=2000, default=None)
    state = models.CharField(max_length=64, default=None)


class ApplyOrder(models.Model):
    user_id = models.IntegerField(default=0)
    reason = models.TextField(max_length=2000, default=None)
    state = models.CharField(max_length=64, default=None)
    # failed passed waiting 默认waiting、


class Comment(models.Model):
    username_from = models.CharField(max_length=64, default=None)
    username_to = models.CharField(max_length=64, default=None)
    content = models.TextField(max_length=2000, default=None)
    time = models.DateTimeField(max_length=64, default=None)


class Judgement(models.Model):
    username = models.CharField(max_length=64, default=None)
    device_id = models.IntegerField(default=None)
    device_name = models.CharField(max_length=64, default=None)
    reason = models.TextField(max_length=2000, default=None)
    time = models.DateTimeField(max_length=64, default=None)


class Dialog(models.Model):
    content = models.TextField(max_length=2000, default=None)
    time = models.DateTimeField(max_length=64, default=None)
