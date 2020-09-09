from django.contrib import admin
from .models import User, Device, RentingOrder

# Register your models here.
admin.site.register(User)
admin.site.register(Device)
admin.site.register(RentingOrder)
