from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from database import models

def GetOrderList(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        size = request.GET.get('size')
        valid = request.GET.get('valid')
        answer_list = []  #最终返回的列表
        if valid == 'passed':
            order_list = models.RentingOrder.objects.filter(valid='passed')
        elif valid == 'failed':
            order_list = models.RentingOrder.objects.filter(valid='failed')
        elif valid == 'waited':
            order_list = models.RentingOrder.objects.filter(valid='waited')
        else:
            order_list = models.RentingOrder.objects.all()

        for i in range((page-1)*size,page*size+1):
            order=order_list[i]
            device=models.Device.objects.get(id=order.device_id)
            part_answer={}#记录此返回消息的字典
            part_answer['orderid']=order.id
            part_answer['devicename'] = device.device_name
            part_answer['owner'] = device.owner
            part_answer['applicant'] = order.username
            part_answer['start'] = order.start
            part_answer['due']=order.due
            part_answer['location']=device.location
            part_answer['addition']=device.addition
            part_answer['state']=device.valid

            answer_list.append(part_answer)
        total = len(answer_list)
        return JsonResponse({})


    else:
        return JsonResponse({'error':'require GET'})