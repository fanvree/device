from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from database import models


# Create your views here.
# def login(request):
#     if request.method == 'POST':
#         username =


def get_user_info(request):         # for admin
    if request.method == 'GET':
        username = request.GET.get('username')
        page = request.GET.get('page')
        size = request.GET.get('size')
        total = len(models.User.objects.all())
        if not size or size < 0:
            return JsonResponse({'error': 'empty data for undefined or negative size'})
        if size == 0:
            size = total
        if not page or page <= 0 or (page - 1) * size > total:
            return JsonResponse({'error': 'empty data for undefined or illegal page'})
        if not username:
            return JsonResponse({'error': 'empty data for undefined or illegal username'})
        user_list = models.User.objects.all()
        first = (page - 1) * size
        last = max(page * size, total)
        user_list = user_list[first: last]
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


def get_device(request):
    # TODO: add identity verification
    if request.method == 'GET':
        page = request.GET.get('page') if request.GET.get('page') != None else 1
        size = request.GET.get('size') if request.GET.get('size') != None else 10
        valid = request.GET.get('valid') if request.GET.get('valid') != None else 'none'
        device_name = request.GET.get('divicename')

        if device_name == None:
            device_list = models.Device.objects.all()
        else:
            device_list = models.Device.objects.filter(device_name=device_name)
        if valid != 'none':
            device_list = device_list.filter(valid=valid)
        total = len(device_list)

        if not size or size < 0:
            return JsonResponse({'error': 'empty data for undefined or negative size'})
        if size == 0:
            size = total
        if not page or page <= 0 or (page - 1) * size > total:
            return JsonResponse({'error': 'empty data for undefined or illegal page'})
        first = (page - 1) * size
        last = max(page * size, total)
        device_list = device_list[first: last]
        d_list = []
        for device in device_list:
            d = {}
            d['deviceid'] = device.id
            d['devicename'] = device.device_name
            d['owner'] = device.owner
            d['phone'] = device.owner_phone
            d['user'] = device.user
            d['start'] = device.start
            d['due'] = device.due
            d['location'] = device.location
            d['addition'] = device.addition
            d['valid'] = device.valid
            d['reason'] = device.reason
            d_list.append(d)

        return JsonResponse({
            'total': total,
            'devicelist': device_list,
        })


def get_owned_device(request):
    if request.method == 'GET':
        page = request.GET.get('page') if request.GET.get('page') != None else 1
        size = request.GET.get('size') if request.GET.get('size') != None else 10
        if not size or size < 0:
            return JsonResponse({'error': 'empty data for undefined or negative size'})
        # if size == 0:
        #     size = total
        # if not page or page <= 0 or (page - 1) * size > total:
        #     return JsonResponse({'error': 'empty data for undefined or illegal page'})
        # TODO:
