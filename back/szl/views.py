from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from database import models

def GetOrderList(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        size = request.GET.get('size')
        valid = request.GET.get('valid')
        order_list = []  #获得的列表
        answer_list = []  #最终返回的列表
        if valid == 'passed':
            order_list = models.RentingOrder.objects.filter(valid='passed')
        elif valid == 'failed':
            order_list = models.RentingOrder.objects.filter(valid='failed')
        elif valid == 'waited':
            order_list = models.RentingOrder.objects.filter(valid='waited')
        else:
            order_list = models.RentingOrder.objects.all()

        

    else:
        return JsonResponse({'error':'require GET'})