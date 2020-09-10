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
        elif valid == 'waiting':
            order_list = models.RentingOrder.objects.filter(valid='waited')
        else:
            order_list = models.RentingOrder.objects.all()

        for i in range((page-1)*size,page*size):
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
        return JsonResponse({'total':total,'orderlist':answer_list})
    else:
        return JsonResponse({'error':'require GET'})

def ChangeOrderState(request):
    if request.method=='GET':
        orderid=request.GET.get('orderid')
        state=request.GET.get('state')

        order=models.RentingOrder.objects.get(id=orderid)
        if state==0:
            order.valid='passed'
        elif state==1:
            order.valid='waiting'
        elif state==2:
            order.valid='failed'

        return JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'error': 'require GET'})

def DeleteOrder(request):
    if request.method=='POST':
        orderid=request.POST.get('orderid')
        order=models.RentingOrder.objects.get(id=orderid)
        if order:
            order.delete()
        else:
            return JsonResponse({'error':'order does not exist'})
    else:
        return JsonResponse({'error': 'require POST'})

def ApplyForOffer(request):
    if request.method=='POST':
        userid=request.POST.get('userid')
        reason=request.POST.get('reason')
        models.ApplyOrder.objects.create(user_id=userid,reason=reason,state='waiting')
        return  JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'error': 'require POST'})

def GetOfferList(request):#查看设备提供者申请列表
    if request.method=='GET':
        state=request.GET.get('state')
        if state=='waiting':
            offer_list=models.ApplyOrder.objects.filter(state='waiting')
        elif state=='passed':
            offer_list=models.ApplyOrder.objects.filter(state='passed')
        elif state=='failed':
            offer_list=models.ApplyOrder.objects.filter(state='failed')
        else:
            offer_list=models.ApplyOrder.objects.all()
        page=request.GET.get('page')
        size=request.GET.get('size')
        answer_list=[]
        for i in range((page-1)*size,page*size):
            if (i < len(offer_list) ):
                offer=offer_list[i]
                part_answer={}
                part_answer['offerid']=offer.id
                user=models.User.objects.get(id=offer.user_id)
                part_answer['applicant']=user.username
                part_answer['reason']=offer.reason
                answer_list.append(part_answer)
        total=len(answer_list)
        return JsonResponse({'total':total,'offerlist':answer_list})
    else:
        return JsonResponse({'error': 'require GET'})

def ChangeOfferState(request):
    if request.method=='GET':
        offerid=request.GET.get('offerid')
        state=request.GET.get('state')
        offer=models.ApplyOrder.get(id=offerid)

        if state==0:
            offer.state='passed'
        elif state==1:
            offer.state='waiting'
        elif state==2:
            offer.state='failed'
        else:
            pass

        return JsonResponse({})
    else:
        return JsonResponse({'error': 'require GET'})

def DeleteOffer(request):
    if request.method=='POST':
        offerid=request.POST.get('offerid')
        offer=models.ApplyOrder.get(id=offerid)
        offer.delete()
        return JsonResponse({})
    else:
        return JsonResponse({'error': 'require POST'})





