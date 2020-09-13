from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from database import models
import matplotlib.pyplot as plt
import io
import base64


def GetOrderList(request): #获得用户租借申请的列表
    if request.method == 'GET':
        # page = request.GET.get('page')
        # size = request.GET.get('size')
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
            if not models.Device.objects.filter(id=order.device_id).exists():
                continue
            device=models.Device.objects.get(id=order.device_id)
            part_answer={}#记录此返回消息的字典
            part_answer['orderid']=order.id
            part_answer['devicename'] = device.device_name
            part_answer['owner'] = device.owner
            part_answer['applicant'] = order.username
            part_answer['start'] = str(order.start.year) + '-' + str(order.start.month) + '-' + str(order.start.day)
            part_answer['due']=str(order.start.year) + '-' + str(order.start.month) + '-' + str(order.start.day)
            part_answer['location']=device.location
            # part_answer['addition']=device.addition
            part_answer['addition']=order.reason
            part_answer['valid']=order.valid

            answer_list.append(part_answer)
        total = len(answer_list)
        return JsonResponse({'total':total,'orderlist':answer_list})
    else:
        return JsonResponse({'error':'require GET'})


def conflict(start_time, due_time, device_id):
    for order in models.RentingOrder.objects.filter(device_id=int(device_id), valid='passed'):
        if not (order.due < start_time or due_time < order.start):
            o = {}
            o['start'] = str(order.start.year) + '-' + str(order.start.month) + '-' + str(order.start.day)
            o['due'] = str(order.due.year) + '-' + str(order.due.month) + '-' + str(order.due.day)
            o['username'] = order.username
            o['contact'] = order.contact
            return JsonResponse({
                'error': 'illegal application for duration collision',
                'order': o
            })
    return False


def ChangeOrderState(request): #改变RentingOrder的状态
    if request.method=='GET':
        orderid=request.GET.get('orderid')
        state=int(request.GET.get('state'))

        order=models.RentingOrder.objects.get(id=orderid)
        device=models.Device.objects.get(id=order.device_id)
        print(orderid,' ',state)
        if state==0:#改变device的valid和user
            if conflict(order.start, order.due, device.id) != False:
                return conflict(order.start, order.due, device.id)
            order.valid='passed'
            device.valid='renting'
            device.user=order.username
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
            if models.User.objects.filter(id=offer.user_id).exists():
                part_answer['applicant'] = models.User.objects.get(id=offer.user_id).username
            else:
                continue
                # part_answer['applicant'] = '用户' + str(offer.user_id) + '已经删除'
            part_answer['reason']=offer.reason
            answer_list.append(part_answer)
        total=len(answer_list)
        # print(total)
        # print(answer_list)
        return JsonResponse({'total':total,'offerlist':answer_list})
    else:
        return JsonResponse({'error': 'require GET'})

def ChangeOfferState(request):#改变用户申请成为设备提供者的状态，
    if request.method=='GET':
        offerid=request.GET.get('offerid')
        state=int(request.GET.get('state'))
        print(offerid,state)
        offer=models.ApplyOrder.objects.get(id=offerid)
        if not models.User.objects.filter(id=offer.user_id).exists():
            return JsonResponse({"message": "error"})
        user=models.User.objects.get(id=offer.user_id)
        if state==0:#改变user的identitiy
            offer.state='passed'
            user.identity='admin'
        elif state==1:
            offer.state='waiting'
        elif state==2:
            offer.state='failed'
        else:
            print("nochange")
            pass
        offer.save()
        user.save()
        return JsonResponse({})
    else:
        return JsonResponse({'error': 'require GET'})

def DeleteOffer(request):#删除用户成为设备提供者的申请
    if request.method=='POST':
        offerid=request.POST.get('offerid')
        offer=models.ApplyOrder.objects.filter(id=offerid)
        offer.delete()
        return JsonResponse({"message": "ok"})
    else:
        return JsonResponse({'error': 'require POST'})

def GetShelfList(request):#得到设备上架请求列表
    if request.method=='GET':
        # page=request.GET.get('page')
        # size=request.GET.get('size')
        state = request.GET.get('state')

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
            if models.Device.objects.filter(id=shelf.device_id).exists():
                device=models.Device.objects.get(id=shelf.device_id)
            else:
                continue
            part_answer['devicename']=device.device_name
            part_answer['location']=device.location
            part_answer['addition']=device.addition
            part_answer['reason']=shelf.reason
            part_answer['state']=shelf.state

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
    labels='off shelf' ,'on shelf','renting','waiting approve'
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
    #num_sum=num_on_order+num_renting+num_on_shelf+num_off_shelf
    sizes=[num_off_shelf,num_on_shelf,num_renting,num_on_order]
    #sizes=[25,25,25,25]
    explode=(0,0,0,0.1)
    fig1,ax1=plt.subplots()
    ax1.pie(sizes,explode=explode,labels=labels,
            autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')
    canvas = fig1.canvas
    print(canvas)
    buffer = io.BytesIO()
    canvas.print_png(buffer)
    data = buffer.getvalue()
    buffer.close()

    labels2='admin','owner','user'
    num_admin=0
    num_owner=0
    num_user=0
    Users=models.User.objects.all()
    for user in Users:
        if user.identity=='admin':
            num_admin=num_admin+1
        elif user.identity=='renter':
            num_owner=num_owner+1
        elif user.identity=='normal':
            num_user=num_user+1
        else:
            pass
    #user_sum=num_admin+num_owner+num_user
    sizes2 = [num_admin,num_owner,num_user]
    explode2 = (0.1,0,0)
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes2, explode=explode2, labels=labels2,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.axis('equal')
    canvas2 = fig2.canvas
    print(canvas2)
    buffer = io.BytesIO()
    canvas2.print_png(buffer)
    data2 = buffer.getvalue()
    buffer.close()

    labels3='passed','failed','waiting'
    num_passed=0
    num_failed=0
    num_waiting=0
    RentOrders=models.RentingOrder.objects.all()
    for rentorder in RentOrders:
        if rentorder.valid=='passed':
            num_passed=num_passed+1
        elif rentorder.valid=='failed':
            num_failed=num_failed+1
        elif rentorder.valid=='waiting':
            num_waiting=num_waiting+1
        else:
            pass
    #sum3=num_passed+num_failed+num_waiting
    sizes3 = [num_passed , num_owner, num_user]
    explode3=(0,0,0.1)
    fig3, ax3 = plt.subplots()
    ax3.pie(sizes3, explode=explode3, labels=labels3,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax3.axis('equal')
    canvas3 = fig3.canvas
    print(canvas3)
    buffer = io.BytesIO()
    canvas3.print_png(buffer)
    data3 = buffer.getvalue()
    buffer.close()
    datalist=[data,data2,data3]



    # plt.show()

    resp = HttpResponse(datalist)
    resp["Content-Type"] = "image/jpeg"
    return resp