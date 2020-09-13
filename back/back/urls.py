
from django.contrib import admin
from django.urls import path
from fzr.views import send_email
from fzr.views import send_email, my
from fzr.views import logon
from fzr.views import owner_mine
from fzr.views import owner_device_add
from fzr.views import owner_device_change
from fzr.views import owner_order_list
from fzr.views import owner_device_order_change
from fzr.views import owner_device_waiting
from fzr.views import add_judgement
from fzr.views import send_judgement
from fzr.views import list_judgement
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
from zsw.views import get_device_reserved_info
from zsw.views import get_application_message
from zsw.views import get_renting_message
from zsw.views import get_shelf_message
from zsw.views import send_comment
from zsw.views import receive_comment

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
    url(r'^owner/device/waiting$', owner_device_waiting),
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
    url(r'^user/apply$', apply_to_be_offer),
    url(r'^user/device/reserved$', get_device_reserved_info),
    url(r'^message/apply$', get_application_message),
    url(r'^message/rent$', get_renting_message),
    url(r'^message/shelf$', get_shelf_message),
    url(r'^comment/send$', send_comment),
    url(r'^comment/receive$', receive_comment),
    url(r'^my$', my),
    url(r'^boss/static$', views.Statistics),
    url(r'^device/judgement/add$', add_judgement),
    url(r'^device/judgement/send$', send_judgement),
    url(r'^device/judgement/list$', list_judgement),
]
