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
    return JsonResponse({"1": "1"})
