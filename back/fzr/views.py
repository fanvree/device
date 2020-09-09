from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import random
from django.contrib.auth.hashers import make_password, check_password
import time


def send_email(request):
    return JsonResponse({'1': '1'})
