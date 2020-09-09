from django.db import models
import datetime

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=1000, default=None)
    email = models.CharField(max_length=64, default=None)
    contact = models.CharField(max_length=64, default=None)
    identity = models.CharField(max_length=64, default=None)
    apply = models.CharField(max_length=64, default=None)
    token = models.CharField(max_length=64, default=None)


class Device(models.Model):
    device_name = models.CharField(max_length=64, default=None)
    owner = models.CharField(max_length=64, default=None)
    owner_phone = models.CharField(max_length=64, default=None)
    user = models.CharField(max_length=64, default=None)
    # rent_out = models.CharField(default=False)
    start = models.DateTimeField(default=datetime.datetime.now())    # TODO
    due = models.DateTimeField(default=datetime.datetime.now())
    location = models.CharField(max_length=64, default=None)
    addition = models.CharField(max_length=64, default=None)
    valid = models.CharField(max_length=64, default=None)
    reason = models.CharField(max_length=64, default=None)


class RentingOrder(models.Model):
    device_id = models.IntegerField(default=0)
    username = models.CharField(max_length=64, default=None)
    reason = models.TextField(max_length=2000, default=None)
    contact = models.TextField(max_length=64, default=None)
    start = models.DateTimeField(max_length=64, default=None)
    due = models.DateTimeField(max_length=64, default=None)


# class ShelfOrder(models.Model):
#     device_id = models.IntegerField(default=0)
#     owner_name = models.CharField(max_length=64, default=None)

