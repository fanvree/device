from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from database import models
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import io
import PIL
from PIL import Image,ImageFont,ImageDraw
from flask import request

def GetOrderList(request): #获得用户租借申请的列表
    if request.method == 'GET':
        valid = request.GET.get('valid')
        answer_list = []  #最终返回的列表
        # order_list，根据valid信息取出来RentingOrder列表
        if valid == 'passed':
            order_list = models.RentingOrder.objects.filter(valid='passed')
        elif valid == 'failed':
            order_list = models.RentingOrder.objects.filter(valid='failed')
        elif valid == 'waiting':
            order_list = models.RentingOrder.objects.filter(valid='waited')
        else:
            order_list = models.RentingOrder.objects.all()

        #根据页数和个数得到相应的RentingOrder，再转成字典、压入列表
        for order in order_list:
            device=models.Device.objects.get(id=order.device_id)
            part_answer={}#记录此返回消息的字典
            part_answer['orderid']=order.id
            part_answer['devicename'] = device.device_name
            part_answer['owner'] = device.owner
            part_answer['applicant'] = order.username
            part_answer['start'] = order.start
            part_answer['due']=order.due
            part_answer['location']=device.location
            # part_answer['addition']=device.addition
            part_answer['addition']=order.reason
            part_answer['valid']=order.valid

            answer_list.append(part_answer)
        total = len(answer_list)
        return JsonResponse({'total':total,'orderlist':answer_list})
    else:
        return JsonResponse({'error':'require GET'})

def ChangeOrderState(request): #改变RentingOrder的状态
    if request.method=='GET':
        orderid=request.GET.get('orderid')
        state=int(request.GET.get('state'))

        order=models.RentingOrder.objects.get(id=orderid)
        device=models.Device.objects.get(id=order.device_id)
        print(orderid,' ',state)
        if state==0:#改变device的valid和user
            order.valid='passed'
            #device.valid='renting'
            #device.user=order.username
        elif state==1:#如果是等待或者失败则不更改device的状态
            order.valid='waiting'
        elif state==2:
            order.valid='failed'
        print(orderid, ' ',order.valid)
        order.save()
        device.save()
        return JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'error': 'require GET'})

def DeleteOrder(request):#删除RentingOrder。所做的操作只是删除
    if request.method=='POST':
        orderid=request.POST.get('orderid')
        order=models.RentingOrder.objects.get(id=orderid)
        if order:
            order.delete()
            return JsonResponse({'message':'ok'})
        else:
            return JsonResponse({'error':'order does not exist'})
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
        #page=request.GET.get('page')
        #size=request.GET.get('size')
        answer_list=[]
        for offer in offer_list:
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

def ChangeOfferState(request):#改变用户申请成为设备提供者的状态，
    if request.method=='GET':
        offerid=request.GET.get('offerid')
        state=request.GET.get('state')
        print(offerid,state)
        offer=models.ApplyOrder.objects.get(id=offerid)
        user=models.User.objects.get(id=offer.user_id)
        if state==0:#改变user的identitiy
            offer.state='passed'
            user.identity='admin'
        elif state==1:
            offer.state='waiting'
        elif state==2:
            offer.state='failed'
        else:
            pass

        return JsonResponse({})
    else:
        return JsonResponse({'error': 'require GET'})

def DeleteOffer(request):#删除用户成为设备提供者的申请
    if request.method=='POST':
        offerid=request.POST.get('offerid')
        offer=models.ApplyOrder.objects.get(id=offerid)
        offer.delete()
        return JsonResponse({"message": "ok"})
    else:
        return JsonResponse({'error': 'require POST'})

def GetShelfList(request):#得到设备上架请求列表
    if request.method=='GET':
        #page=request.GET.get('page')
        #size=request.GET.get('size')
        state=request.GET.get('state')

        if state=='waiting':
            tmp_shelf_list=models.ShelfOrder.objects.filter(state='waiting')
        elif state=='passed':
            tmp_shelf_list = models.ShelfOrder.objects.filter(state='passed')
        elif state=='failed':
            tmp_shelf_list = models.ShelfOrder.objects.filter(state='failed')
        else:
            tmp_shelf_list = models.ShelfOrder.objects.all()

        answer_list=[]
        for shelf in tmp_shelf_list:
            part_answer={}
            part_answer['shelfid']=shelf.id
            part_answer['ownername']=shelf.owner_name

            device=models.Device.objects.get(id=shelf.device_id)
            part_answer['devicename']=device.device_name
            part_answer['location']=device.location
            part_answer['addition']=device.addition
            part_answer['reason']=shelf.reason

            answer_list.append(part_answer)
        total=len(answer_list)
        return JsonResponse({'total':total,'shelflist':answer_list})
    else:
        return JsonResponse({'error':'require GET'})

def ChangeShelfState(request):#状态变化请求
    if request.method=='GET':
        shelfid=request.GET.get('shelfid')
        state=int(request.GET.get('state'))
        if not models.ShelfOrder.objects.filter(id=shelfid).exists():
            return JsonResponse({"error": "no exists"})
        shelf=models.ShelfOrder.objects.get(id=shelfid)
        if not models.Device.objects.filter(id=shelf.device_id).exists():
            return JsonResponse({"error": "no exists"})
        device=models.Device.objects.get(id=shelf.device_id)
        if state==0:
            shelf.state='passed'
            device.valid='on_shelf'#如果通过，将设备的状态变为上架
        elif state==1:
            shelf.state='waiting'
            device.valid='on_order'#如果还是在等待，仍然设置成on_order
        elif state==2:
            shelf.state='failed'
            device.valid='off_shelf'#如果被拒绝，下架状态
        else:
            pass
        shelf.save()
        device.save()
        return JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'error':'require GET'})

def DeleteShelf(request):#删除上架申请
    if request.method=='POST':
        shelfid=request.POST.get('shelfid')
        if not models.ShelfOrder.objects.filter(id=shelfid).exists():
            return JsonResponse({'error': 'no shelfid'})
        shelf=models.ShelfOrder.objects.get(id=shelfid)
        shelf.delete()
        return JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'error':'require POST'})

def Statistics(request):
    labels='下架','在架','借出','等待审批'
    num_off_shelf=0
    num_on_shelf=0
    num_renting=0
    num_on_order=0
    Devices=models.Device.objects.all()
    for device in Devices:
        valid=device.valid
        if valid=='off_shelf':
            num_off_shelf=num_off_shelf+1
        elif valid=='on_shelf':
            num_on_shelf=num_on_shelf+1
        elif valid=='renting':
            num_renting=num_renting+1
        elif valid=='on_order':
            num_on_order=num_on_order+1
        else:
            pass
    num_sum=num_on_order+num_renting+num_on_shelf+num_off_shelf
    sizes=[num_off_shelf*100/num_sum,num_on_shelf*100/num_sum,num_renting*100/num_sum,num_on_order*100/num_sum]
    #sizes=[25,25,25,25]
    explode=(0,0,0,0.1)
    fig1,ax1=plt.subplots()
    ax1.pie(sizes,explode=explode,labels=labels,
            autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')

    plt.show()
    canvas=fig1.canvas

    buffer=io.BytesIO()
    canvas.print_png(buffer)
    data=buffer.getvalue()
    buffer.close()

    return render({'pie':data})




