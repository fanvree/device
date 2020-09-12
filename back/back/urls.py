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
from zsw.views import login
from zsw.views import logout
from zsw.views import get_user
from zsw.views import delete_user
from zsw.views import set_user
from zsw.views import get_device
from zsw.views import delete_device
from zsw.views import edit_device
from zsw.views import get_shelf_device
from zsw.views import order_device
from zsw.views import get_order_history
from zsw.views import get_self_rented_device

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sendemail$', send_email),
    url(r'^logon$', logon),
    url(r'^boss/order/list$', views.GetOrderList),
    url(r'^boss/order/state$', views.ChangeOrderState),
    url(r'^boss/order/delete$', views.DeleteOrder),
    url(r'^boss/offer/list$', views.GetOfferList),
    url(r'^boss/offer/state$', views.ChangeOfferState),
    url(r'^boss/offer/delete$', views.DeleteOffer),
    url(r'^boss/shelf/list$', views.GetShelfList),
    url(r'^boss/shelf/state$', views.ChangeShelfState),
    url(r'^boss/shelf/delete$', views.DeleteShelf),
    url(r'^boss/order/list$', views.GetOrderList),
    url(r'^boss/order/state$', views.ChangeOrderState),
    url(r'^boss/order/delete$', views.DeleteOrder),
    url(r'^owner/device/mine$', owner_mine),
    url(r'^owner/device/add$', owner_device_add),
    url(r'^owner/device/change$', owner_device_change),
    url(r'^owner/device/order$', owner_order_list),
    url(r'^owner/device/order/change$', owner_device_order_change),
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^boss/user/list$', get_user),
    url(r'^boss/user/delete$', delete_user),
    url(r'^boss/user/set$', set_user),
    url(r'^boss/device/list$', get_device),
    url(r'^boss/device/delete$', delete_device),
    url(r'^boss/device/change$', edit_device),
    url(r'^user/device/list$', get_shelf_device),
    url(r'^user/device/lend$', order_device),
    url(r'^user/order/history$', get_order_history),
    url(r'^user/device/own$', get_self_rented_device)
]
=======
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
from zsw.views import login
from zsw.views import logout
from zsw.views import get_user
from zsw.views import delete_user
from zsw.views import set_user
from zsw.views import get_device
from zsw.views import delete_device
from zsw.views import edit_device
from zsw.views import get_shelf_device
from zsw.views import order_device
from zsw.views import get_order_history
from zsw.views import get_self_rented_device
from zsw.views import apply_to_be_offer

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sendemail$', send_email),
    url(r'^logon$', logon),
    url(r'^boss/order/list$', views.GetOrderList),
    url(r'^boss/order/state$', views.ChangeOrderState),
    url(r'^boss/order/delete$', views.DeleteOrder),
    url(r'^boss/offer/list$', views.GetOfferList),
    url(r'^boss/offer/state$', views.ChangeOfferState),
    url(r'^boss/offer/delete$', views.DeleteOffer),
    url(r'^boss/shelf/list$', views.GetShelfList),
    url(r'^boss/shelf/state$', views.ChangeShelfState),
    url(r'^boss/shelf/delete$', views.DeleteShelf),
    url(r'^boss/order/list$', views.GetOrderList),
    url(r'^boss/order/state$', views.ChangeOrderState),
    url(r'^boss/order/delete$', views.DeleteOrder),
    url(r'^owner/device/mine$', owner_mine),
    url(r'^owner/device/add$', owner_device_add),
    url(r'^owner/device/change$', owner_device_change),
    url(r'^owner/device/order$', owner_order_list),
    url(r'^owner/device/order/change$', owner_device_order_change),
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^boss/user/list$', get_user),
    url(r'^boss/user/delete$', delete_user),
    url(r'^boss/user/set$', set_user),
    url(r'^boss/device/list$', get_device),
    url(r'^boss/device/delete$', delete_device),
    url(r'^boss/device/change$', edit_device),
    url(r'^user/device/list$', get_shelf_device),
    url(r'^user/device/lend$', order_device),
    url(r'^user/order/history$', get_order_history),
    url(r'^user/device/own$', get_self_rented_device),
    url(r'^user/apply$', apply_to_be_offer)
]
