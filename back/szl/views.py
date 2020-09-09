from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from database import models

def GetOrderList(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        size = request.GET.get('size')
        valid = request.GET.get('valid')
        order_list = models.RentingOrder.objects.all()

    else:
        return JsonResponse({'error':'require GET'})