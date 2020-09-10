"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fzr.views import send_email
from fzr.views import logon
from fzr.views import owner_mine
from fzr.views import owner_device_add
from fzr.views import owner_device_change
from fzr.views import owner_order_list
from fzr.views import owner_device_order_change
from django.conf.urls import url
from szl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sendemail$', send_email),
    url(r'^logon$', logon),
    url(r'^boss/order/list$', views.GetOrderList),
    url(r'^boss/order/state$', views.ChangeOrderState),
    url(r'^boss/order/delete$', views.DeleteOrder),
    url(r'^owner/device/mine$', owner_mine),
    url(r'^owner/device/add$', owner_device_add),
    url(r'^owner/device/change$', owner_device_change),
    url(r'^owner/device/order$', owner_order_list),
    url(r'^owner/device/order/change$', owner_device_order_change),
]
