from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


# Create your views here.
def get_user_info(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        page = request.GET.get('page')
        size = request.GET.get('size')
        if size <= 0:
            return JsonResponse({'error': 'empty data because of negative size'})
        if page <= 0:
            return JsonResponse({'error': 'empty data because of negative page'})

