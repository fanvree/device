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


def send_email(request):
    print(request.GET)
    if 'email' in request.GET:
        mail = request.GET['email']
        if validate_email(mail):
            send_register_email(mail, gen_code(mail))
            return JsonResponse({'ok': 'ok'})
    return JsonResponse({'error': 'error'})


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
                return JsonResponse({"success": "add into user list"})
            else:
                return JsonResponse({"error": "code is error"})
        return JsonResponse({"error": "username is exist"})
    return JsonResponse({"error": "变量不够"})


def owner_mine(request):
    page = 1
    size = 10
    valid = -1
    device_name = ''
    if 'page' in request.GET:
        page = int(request.GET['page'])
    if 'size' in request.GET:
        size = int(request.GET)
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
                    # 'reason': item.reason,
                })
    return JsonResponse(ret_list)


def owner_device_add(request):
    if 'devicelist' in request.POST:
        device_list = request.POST['devicelist']
        for item in device_list:
            if request.POST['owner']:
                device = Device()
                device.device_name = request.POST['devicename']
                device.owner = request.POST['owner']
                device.owner_phone = request.POST['ownerphone']
                device.user = ''
                device.start = None
                device.due = None
                device.location = request.POST['location']
                device.addition = request.POST['addition']
                device.valid = '1'
                device.reason = request.POST['reason']
                device.save()



