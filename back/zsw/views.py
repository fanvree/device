from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from database import models
from datetime import date


# Create your views here.
# 1.3.3: for all users: login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 用户名参数不存在或者为空，或者此用户不存在
        if username == None or username == '' or not models.User.objects.filter(username=username).exists():
            return JsonResponse({'state': 'empty'})
        # 密码不匹配
        if not check_password(password, models.User.objects.get(username=username).password):
            return JsonResponse({'state': 'not matched'})
        # 当前已经处于登录状态
        if 'is_login' in request.session and request.session['is_login']:
            return JsonResponse({'state': 'already online'})

        request.session['username'] = username
        request.session['is_login'] = True
        return JsonResponse({'state': 1})


# 1.3.4: for all users: logout
def logout(request):
    if request.method == 'POST':
        if 'is_login' in request.session.keys() and request.session['is_login']:
            username = request.session['username']
            del request.session['is_login']
            del request.session['username']
            return JsonResponse({'state': 1})   # success
        else:                   # session_id不存在或被注销
            return JsonResponse({'state': 0})   # fail


# 1.1.1: for admin: to get users under various filters
def get_user(request):
    if request.method == 'GET':
        admin = models.User.objects.get(username=request.session['username'])
        if admin.identity != 'admin':
            return JsonResponse({'error': 'low permission'})

        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'empty data for undefined or illegal username'})
        user_list = models.User.objects.filter(username__contains=username)
        total = len(user_list)

        u_list = []
        for user in user_list:
            u = {}
            u['userid'] = user.id
            u['username'] = user.username
            u['identity'] = user.identity
            u['contact'] = user.contact
            u['email'] = user.email
            u_list.append(u)
        return JsonResponse({
            'total': total,
            'userlist': u_list,
        })


# TODO: test
# 1.1.2: for admin: delete users
def delete_user(request):
    if request.method == 'POST':
        admin = models.User.objects.get(username=request.session['username'])
        if admin.identity != 'admin':
            return JsonResponse({'error': 'low permission'})

        userid = request.POST.get('userid')
        if userid == None:
            return JsonResponse({'error': 'userid'})
        userid = int(userid)
        if not models.User.objects.filter(id=userid).exists():
            return JsonResponse({'error': 'user non-existence'})

        username = models.User.objects.get(id=userid)
        if models.RentingOrder.objects.filter(username=username, rent_state='renting').exists():
            return JsonResponse({'error': 'the user is using a device'})
        models.User.objects.get(id=userid).delete()
        return JsonResponse({'ok': 'deleted'})


# 1.1.3: for admin: set users' identity
def set_user(request):
    if request.method == 'POST':
        admin = models.User.objects.get(username=request.session['username'])
        if admin.identity != 'admin':
            return JsonResponse({'error': 'low permission'})

        userid = request.POST.get('userid')
        identity = request.POST.get('identity')
        if userid == None:
            return JsonResponse({'error': 'userid missing'})
        if not models.User.objects.filter(id=userid).exists():
            return JsonResponse({'error': 'user non-existence'})
        if identity == None or identity not in ('normal', 'owner', 'admin'):
            return JsonResponse({'error': 'identity invalid'})
        userid = int(userid)
        user = models.User.objects.get(id=userid)
        user.identity = identity
        user.save()
        return JsonResponse({'ok': 'set'})


# 1.2.1: for admin: to get devices under various filters
def get_device(request):
    if request.method == 'GET':
        admin = models.User.objects.get(username=request.session['username'])
        if admin.identity != 'admin':
            return JsonResponse({'error': 'low permission'})

        valid = request.GET.get('valid') if request.GET.get('valid') != None else 'none'
        device_name = request.GET.get('devicename')

        if device_name == None:
            device_list = models.Device.objects.all()
        else:
            device_list = models.Device.objects.filter(device_name=device_name)
        if valid != 'none':
            device_list = device_list.filter(valid=valid)

        total = len(device_list)
        d_list = []
        for device in device_list:
            d = {}
            d['deviceid'] = device.id
            d['devicename'] = device.device_name
            d['owner'] = device.owner
            d['phone'] = device.owner_phone
            d['location'] = device.location
            d['addition'] = device.addition
            d['valid'] = device.valid
            d['reason'] = device.reason
            d_list.append(d)

        return JsonResponse({
            'total': total,
            'devicelist': d_list,
        })


# 1.2.2: for admin: to edit device with optional choice
def edit_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('deviceid')
        if device_id == None:
            return JsonResponse({'error': 'deviceid missing'})
        device_id = int(device_id)
        if not models.Device.objects.filter(id=device_id).exists():
            return JsonResponse({'error': 'deviceid invalid'})

        device = models.Device.objects.get(id=device_id)
        d = {}
        d['device_name'] = request.POST.get('devicename')
        d['owner'] = request.POST.get('owner')
        d['phone'] = request.POST.get('phone')
        d['location'] = request.POST.get('location')
        d['addition'] = request.POST.get('addition')
        d['valid'] = request.POST.get('valid')
        d['reason'] = request.POST.get('reason')
        for key, value in d.items():
            if value != None:
                setattr(device, key, value)
        device.save()
        return JsonResponse({'ok': 'edited'})


# TODO: test
# 1.2.3: for admin: to delete device
def delete_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('deviceid')
        if device_id == None:
            return JsonResponse({'error': 'deviceid missing'})
        device_id = int(device_id)
        if not models.Device.objects.filter(id=device_id).exists():
            return JsonResponse({'error': 'deviceid invalid'})
        device = models.Device.objects.get(id=device_id)
        if device.valid == 'renting':
            return JsonResponse({'error': 'device is rented'})
        models.Device.objects.get(id=device_id).delete()
        return JsonResponse({'ok': 'deleted'})


# 2.1.0: for normal users: to login or logout, see 1.3.3 & 1.3.4


# 2.2.0: for normal users: to get devices on shelf
def get_shelf_device(request):
    if request.method == 'GET':
        device_name = request.GET.get('divicename')

        if device_name == None:
            device_list = models.Device.objects.all()
        else:
            device_list = models.Device.objects.filter(device_name=device_name)
        device_list = device_list.filter(valid__in=['on_shelf', 'renting'])
        total = len(device_list)

        d_list = []
        for device in device_list:
            d = {}
            d['deviceid'] = device.id
            d['devicename'] = device.device_name
            d['owner'] = device.owner
            d['phone'] = device.owner_phone
            d['location'] = device.location
            d['addition'] = device.addition
            d['valid'] = device.valid
            d['reason'] = device.reason
            d_list.append(d)

        return JsonResponse({
            'total': total,
            'devicelist': d_list,
        })


# 2.3.0: for normal users: to order devices
def order_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('deviceid')
        reason = request.POST.get('reason')
        start = request.POST.get('start')
        due = request.POST.get('due')
        if device_id == None or reason == None or start == None or due == None:
            return JsonResponse({'error': 'parameters missing'})
        start_list = start.split('-')
        due_list = due.split('-')
        start_time = date(year=int(start_list[0]), month=int(start_list[1]), day=int(start_list[2]))
        due_time = date(year=int(due_list[0]), month=int(due_list[1]), day=int(start_list[2]))
        # to prevent illegal renting order resulting from duration collision
        now = timezone.now().date()
        for order in models.RentingOrder.objects.filter(device_id=device_id):
            if (order.start - now).year > 0:        # for the reserved devices doesn't start yet
                if order.start <= start_time <= order.due or start_time <= order.start <= due_time:
                    o = {}
                    o['start'] = order.start
                    o['due'] = order.due
                    o['username'] = order.username
                    o['contact'] = order.contact
                    return JsonResponse({
                        'error': 'illegal application for duration collision',
                        'order': order
                    })
        device_id = int(device_id)
        username = request.session['username']
        contact = models.User.objects.get(username=username).contact
        models.RentingOrder.objects.create(
            device_id=device_id,
            username=username,
            reason=reason,
            contact=contact,
            start=start,
            due=due,
            valid='waiting',
            rent_state='default'
        )
        return JsonResponse({'ok': 'waiting for offer to agree the order'})


# 2.4.0: for normal users: to get his or her renting order history
def get_order_history(request):
    if request.method == 'GET':
        username = request.session['username']
        order_list = models.RentingOrder.objects.filter(user=username)
        total = len(order_list)
        o_list = []
        for order in order_list:
            device = models.Device.objects.get(id=order.device_id)
            o = {}
            o['orderid'] = order.id
            o['devicename'] = device.device_name
            o['owner'] = device.owner
            o['user'] = order.username
            o['start'] = order.start
            o['due'] = order.due
            o['location'] = device.location
            o['addition'] = device.addition
            o['state'] = order.valid
        return JsonResponse({
            'total': total,
            'orderlist': o_list,
        })


# 2.5.0:for normal users: to get devices he or she has already rented
def get_self_rented_device(request):
    if request.method == 'GET':
        username = request.session['username']
        device_list = models.Device.objects.filter(user=username)

        total = len(device_list)
        d_list = []
        for device in device_list:
            d = {}
            d['deviceid'] = device.id
            d['devicename'] = device.device_name
            d['owner'] = device.owner
            d['phone'] = device.owner_phone
            d['location'] = device.location
            d['addition'] = device.addition
            d['valid'] = device.valid
            d['reason'] = device.reason
            d['orderlist'] = []
            d_list.append(d)
        for order in models.RentingOrder.objects.all():
            for d in d_list:
                if order.device_id == d['deviceid']:
                    o = {}
                    o['username'] = order.username
                    o['reason'] = order.reason
                    o['contact'] = order.contact
                    o['start'] = order.start
                    o['due'] = order.due
                    o['valid'] = o['valid']
                    d['orderlist'].append(o)
        return JsonResponse({
            'total': total,
            'devicelist': d_list,
        })


# 2.6.0:for normal users: to apply for higher identity(offer)
def apply_to_be_offer(request):
    if request.method == 'POST':
        user_id = request.POST.get('userid')
        reason = request.POST.get('reason')
        if user_id == None or reason == None:
            return JsonResponse({'error': 'parameters missing'})
        user_id = int(user_id)
        if user_id != models.User.objects.get(id=request.session['username']):
            return JsonResponse({'error': 'invalid user id'})
        models.ApplyOrder.objects.create(user_id=user_id, reason=reason, state='waiting')
        return JsonResponse({'ok': 'submitted'})


# 2.7.0:for normal users: to get reserved information of one device
def get_device_reserved_info(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceid')
        device = models.Device.objects.get(id=device_id)
        username = request.session['username']
        d = {}
        d['deviceid'] = device.id
        d['devicename'] = device.device_name
        d['owner'] = device.owner
        d['phone'] = device.owner_phone
        d['location'] = device.location
        d['addition'] = device.addition
        d['valid'] = device.valid
        d['reason'] = device.reason
        d['orderlist'] = []

        for order in models.RentingOrder.objects.all():
            o = {}
            o['user'] = order.username
            o['start'] = order.start
            o['due'] = order.due
            o['contact'] = order.contact
            d['orderlist'].append(o)
        return JsonResponse(d)


# from a device id to detailed info of this device
def get_single_device_info(request):
    if request.method == 'GET':
        device_id = request.GET.get('deviceid')
        if not device_id:
            return JsonResponse({'state': 0})
        if not models.Device.objects.filter(id=device_id).exists():
            return JsonResponse({'state': 0})
        device = models.Device.objects.get(id=device_id)
        d = {}
        d['devicename'] = device.device_name
        d['owner'] = device.owner
        d['phone'] = device.owner_phone
        d['location'] = device.location
        d['addition'] = device.addition
        d['valid'] = device.valid
        d['reason'] = device.reason
        return JsonResponse(d)
