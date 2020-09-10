from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import random
from django.contrib.auth.hashers import make_password, check_password
import time
from django.core.mail import send_mail
from django.conf import settings
from database.models import User
from database.models import Device
from database.models import RentingOrder
from database.models import ShelfOrder
from django.utils import timezone


def send_register_email(to, code):
    title = "注册激活链接"
    body = "你的验证码是: {0}".format(code)
    print(body)
    send_mail(title, body, settings.DEFAULT_FROM_EMAIL, [to])


def gen_code(mail):
    ret = 0
    for i in mail:
        ret = (ret * 10 + ord(i)) % 1000000
    ret += 1000000
    return ret


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# 发送邮件
def send_email(request):
    print(request.GET)
    if 'email' in request.GET:
        mail = request.GET['email']
        if validate_email(mail):
            send_register_email(mail, gen_code(mail))
            return JsonResponse({'ok': 'ok'})
    return JsonResponse({'error': 'error'})


# 完成注册
def logon(request):
    if ('username' in request.POST) and ('email' in request.POST) and ('code' in request.POST) and ('password' in request.POST):
        username = request.POST['username']
        if not (User.objects.filter(username=username).exists()):
            email = request.POST['email']
            code = request.POST['code']
            password = request.POST['password']
            if str(gen_code(email)) == str(code):
                user = User()
                user.username = username
                user.password = make_password(password)
                user.email = email
                user.contact = "4008823823"
                user.identity = "normal"
                user.apply = "False"
                user.token = ""
                user.save()
                return JsonResponse({"state": "注册成功"})
            else:
                return JsonResponse({"state": "注册失败code is error"})
        return JsonResponse({"state": "注册失败username is exist"})
    return JsonResponse({"state": "注册失败变量不够"})


# 查看我的设备
# 可以根据devicename进行筛选
# 也可以根据valid状态筛选 0/已经上架但未外借 1/未审核 2/未上架 3/已外借
def owner_mine(request):
    page = 1
    size = 10
    valid = -1
    device_name = ''
    if 'page' in request.GET:
        page = int(request.GET['page'])
    if 'size' in request.GET:
        size = int(request.GET['size'])
    if 'valid' in request.GET:
        valid = int(request.GET['valid'])
    if 'devicename' in request.GET:
        device_name = int(request.GET['devicename'])
    show_list = Device.objects.all()
    total = 0
    ret_list = []
    for item in show_list:
        if (valid == -1 or valid == item.valid) and (device_name == "" or item.device_name.find(device_name) != -1) \
                and item.owner == request.session['username']:
            total += 1
            if ((page - 1) * size < total) and (total < page * size):
                ret_list.append({
                    'deviceid': item.id,
                    'devicename': item.device_name,
                    'owner': item.owner,
                    'phone': item.owner_phone,
                    'user': item.user,
                    'start': item.start,
                    'due': item.due,
                    'location': item.location,
                    'addition': item.addition,
                    'valid': item.valid,
                    'reason': item.reason,
                })
    return JsonResponse(ret_list)


# 增加我的设备
def owner_device_add(request):
    if 'devicelist' in request.POST:
        device_list = request.POST['devicelist']
        for item in device_list:
            if request.POST['owner']:
                device = Device()
                device.device_name = request.POST['devicename']
                device.owner = request.session['username']
                device.owner_phone = request.POST['ownerphone']
                device.user = ''
                device.start = None
                device.due = None
                device.location = request.POST['location']
                device.addition = request.POST['addition']
                device.valid = '1'
                device.reason = request.POST['reason']
                device.save()
                # shelf_order
                shelf_order = ShelfOrder()
                shelf_order.device_id = device.id
                shelf_order.owner_name = device.owner
                shelf_order.reason = device.reason
                shelf_order.state = '1'
                shelf_order.start_time = timezone.now()
                shelf_order.save()


# 改变我的设备状态： 0已归还 1未审核 2未上架 3已外借 4删除
def owner_device_change(request):
    if request.method == 'GET' and 'deviceid' in request.GET and 'valid' in request.GET:
        device_id = int(request.GET['deviceid'])
        valid = int(request.GET['valid'])
        if Device.objects.filter(device_id=device_id).exists():
            device = Device.objects.get(device_id=device_id)
            if valid == 4:
                Device.objects.filter(device_id=device_id).delete()
            elif valid == 1:
                device.valid = valid
                device.save()
            else:
                device.valid = valid
                device.save()
            return JsonResponse({"ok": "setting ok"})
        return JsonResponse({"error": "no deviceid"})
    return JsonResponse({"error": "valid parse"})


# 查询订单列表： 可以筛选 'state': 0/审核通过 1/未审核 2/审核未通过 和
# 'rentstate': 0/审核通过，未借出   1/已经借出  2/已经归还 的情况
# deviceid 查看某个设备的订单
def owner_order_list(request):
    if request.method == 'GET':
        page = 1
        size = 10
        device_id = -1
        valid = -1
        rent_state = -1
        if 'page' in request.GET:
            page = int(request.GET['page'])
        if 'size' in request.GET:
            size = int(request.GET['size'])
        if 'deviceid' in request.GET:
            device_id = int(request.GET['deviceid'])
        if 'state' in request.GET:
            valid = int(request.GET['state'])
        if 'state' in request.GET:
            rent_state = int(request.GET['rentstate'])
        total = 0
        ret = []
        for renting_order in RentingOrder.objects.all():
            if Device.objects.filter(renting_order.device_id).exists():
                device = Device.objects.get(renting_order.device_id)
                owner = device.owner
                device_name = device.device_name
                location = device.location
                if owner == request.session['username'] and \
                        (device_id == -1 or device_id == renting_order.device_id) and \
                        (valid == -1 or valid == renting_order.valid) and \
                        (rent_state == -1 or rent_state == renting_order.rent_state):
                    total += 1
                    if ((page - 1) * size < total) and (total <= page * size):
                        ret.append({
                            'ordid': renting_order.id,
                            'devicename': device_name,
                            'owner': owner,
                            'applicant': renting_order.username,
                            'start': renting_order.start,
                            'due': renting_order.due,
                            'location': location,
                            'addition': renting_order.reason,
                            'state': renting_order.valid,
                            'rentstate': renting_order.rent_state,
                            'rentstart': renting_order.rent_start,
                            'rentend': renting_order.rent_end,
                        })
        return JsonResponse({'orderlist': ret, 'total': total})


# 改变orderid订单状态：state 0/审核通过 1/未审核 2/审核未通过
# 'rentstate': 0/审核通过，未借出   1/已经借出  2/已经归还 的情况
def owner_device_order_change(request):
    if request.method == 'GET':
        order_id = int(request.GET['orderid'])
        state = int(request.GET.get('state')) if request.GET.get('state') is not None else -1
        rent_state = int(request.GET.get('rentstate')) if request.GET.get('rentstate') is not None else -1
        if RentingOrder.objects.filter(order_id=order_id).exists():
            renting_order = RentingOrder.objects.get(order_id=order_id)
            if state != -1:
                renting_order.valid = state
            if rent_state != -1:
                renting_order.rent_state = rent_state
                if rent_state == 1:
                    renting_order.rent_start = timezone.now()
                    if Device.objects.filter(device_id=renting_order.device_id).exists():
                        device = Device.objects.get(device_id=renting_order.device_id)
                        device.valid = 3
                        device.save()
                elif rent_state == 2:
                    renting_order.rent_end = timezone.now()
                    if Device.objects.filter(device_id=renting_order.device_id).exists():
                        device = Device.objects.get(device_id=renting_order.device_id)
                        device.valid = 0
                        device.save()
            renting_order.save()
        return JsonResponse({'ok': 'ok'})


def my(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    userid = user.id
    identity = user.identity
    return JsonResponse({
        'username': username,
        'userid': userid,
        'identity': identity,
    })







