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
            return JsonResponse({'state': '1'})
    return JsonResponse({'state': '0'})


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
# 也可以根据valid状态筛选 on_shelf/已经上架但未外借0 on_order/未审核1 off_shelf/未上架2 renting/已外借3
def owner_mine(request):
    page = 1
    size = 10000
    valid = 'none'
    device_name = ''
    # if 'page' in request.GET:
    #     page = int(request.GET['page'])
    # if 'size' in request.GET:
    #     size = int(request.GET['size'])
    if 'valid' in request.GET:
        valid = request.GET['valid']
    if 'devicename' in request.GET:
        device_name = int(request.GET['devicename'])
    show_list = Device.objects.all()
    total = 0
    ret_list = []
    for device in show_list:
        if (valid == 'none' or valid == device.valid) and (device_name == "" or device.device_name.find(device_name) != -1) \
                and device.owner == request.session['username']:
            total += 1
            if ((page - 1) * size < total) and (total < page * size):
                ret_list.append({
                    'deviceid': device.id,
                    'devicename': device.device_name,
                    'owner': device.owner,
                    'phone': device.owner_phone,
                    # 'user': device.user,
                    # 'start': device.start,
                    # 'due': device.due,
                    'location': device.location,
                    'addition': device.addition,
                    'valid': device.valid,
                    'reason': device.reason,
                })
    return JsonResponse(ret_list)


# 增加我的设备
# 'valid':'none','passed','failed','waited'
def owner_device_add(request):
    if request.method == 'POST':
        device = Device()
        device.device_name = request.POST['devicename']
        device.owner = request.session['username']
        device.owner_phone = request.POST['phone']
        # device.user = ''
        # device.start = timezone.now().date()
        # device.due = timezone.now().date()
        device.location = request.POST['location']
        device.addition = request.POST['addition']
        device.valid = 'on_order'
        device.reason = request.POST['reason']
        device.save()
        # shelf_order
        shelf_order = ShelfOrder()
        shelf_order.device_id = device.id
        shelf_order.owner_name = device.owner
        shelf_order.reason = device.reason
        shelf_order.state = 'waiting'
        shelf_order.start_time = timezone.now().date()
        shelf_order.save()
        return JsonResponse({'message': 'ok'})


# 改变我的设备状态：
def owner_device_change(request):
    if request.method == 'GET' and 'deviceid' in request.GET and 'valid' in request.GET:
        device_id = int(request.GET['deviceid'])
        valid = request.GET['valid']
        if Device.objects.filter(id=device_id).exists():
            device = Device.objects.get(id=device_id)
            if valid == 'delete':
                Device.objects.filter(id=device_id).delete()
            else:
                device.valid = valid
                device.save()
            return JsonResponse({"ok": "setting ok"})
        return JsonResponse({"error": "no deviceid"})
    return JsonResponse({"error": "valid parse"})


# 查询订单列表： 可以筛选 'state': 'valid':'none','passed','failed','waited'
# 'rentstate': 'none'  'default' 'renting'  'back'                 0/审核通过，未借出   1/已经借出  2/已经归还 的情况
# deviceid 查看某个设备的订单
def owner_order_list(request):
    if request.method == 'GET':
        page = 1
        size = 10000
        device_id = -1
        valid = 'none'
        rent_state = 'none'
        # if 'page' in request.GET:
        #     page = int(request.GET['page'])
        # if 'size' in request.GET:
        #     size = int(request.GET['size'])
        if 'deviceid' in request.GET:
            device_id = int(request.GET['deviceid'])
        if 'state' in request.GET:
            valid = request.GET['state']
        if 'rentstate' in request.GET:
            rent_state = int(request.GET['rentstate'])
        total = 0
        ret = []
        for renting_order in RentingOrder.objects.all():
            if Device.objects.filter(id=renting_order.device_id).exists():
                device = Device.objects.get(id=renting_order.device_id)
                owner = device.owner
                device_name = device.device_name
                location = device.location
                if owner == request.session['username'] and \
                        (device_id == -1 or device_id == renting_order.device_id) and \
                        (valid == 'none' or valid == renting_order.valid) and \
                        (rent_state == 'none' or rent_state == renting_order.rent_state):
                    total += 1
                    if ((page - 1) * size < total) and (total <= page * size):
                        ret.append({
                            'ordid': renting_order.id,
                            'deviceid': renting_order.device_id,
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


# 改变orderid订单状态：state 0/审核通过 1/未审核 2/审核未通过   'passed','failed','waited'
# 'rentstate': 0/审核通过，未借出   1/已经借出  2/已经归还 的情况  'default' 'renting'  'back'
def owner_device_order_change(request):
    if request.method == 'GET':
        order_id = int(request.GET['orderid'])
        state = request.GET.get('state') if request.GET.get('state') is not None else 'none'
        rent_state = request.GET.get('rentstate') if request.GET.get('rentstate') is not None else 'none'
        if RentingOrder.objects.filter(id=order_id).exists():
            renting_order = RentingOrder.objects.get(id=order_id)
            if state == 'passed':
                for order in RentingOrder.objects.filter(device_id=renting_order.device_id, valid='passed'):
                    if not (order.due < renting_order.start or renting_order.due < order.start):
                        o = {}
                        o['start'] = order.start
                        o['due'] = order.due
                        o['username'] = order.username
                        o['contact'] = order.contact
                        return JsonResponse({
                            'error': 'illegal application for duration collision',
                            'order': o
                        })
            if state != 'none':
                renting_order.valid = state
            if rent_state != 'none':
                if renting_order.valid != 'passed':
                    return JsonResponse({
                        'error': 'renting order is not passed'
                    })
                renting_order.rent_state = rent_state
                if rent_state == 'renting':
                    renting_order.rent_start = timezone.now().date()
                    if Device.objects.filter(id=renting_order.device_id).exists():
                        device = Device.objects.get(id=renting_order.device_id)
                        device.valid = 'renting'
                        device.save()
                elif rent_state == 'back':
                    renting_order.rent_end = timezone.now().date()
                    if Device.objects.filter(id=renting_order.device_id).exists():
                        device = Device.objects.get(id=renting_order.device_id)
                        device.valid = 'on_shelf'
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







