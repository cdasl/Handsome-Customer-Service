from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string
from . import models
from chatterbot import ChatBot
from .apis.enterprise import *

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def api(request):
    req = json.loads(request.body.decode('utf8'))
    func = eval(req['method'])
    return func(req['data'])

@ensure_csrf_cookie
def enterprise(request):
    return render(request, 'enterprise.html')

@csrf_exempt
def user(request):
    return render(request, 'User.html')