from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string
from .. import models
from chatterbot import ChatBot
from . import helper, messages

@ensure_csrf_cookie
def customer_chatted(request):
    """
        获取与某位客服聊过天的所有用户
    """
    info = {'cid': -1}
    CID = 'cid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and hasattr(request.session, 'cid'):
           CID = request.session['cid']
    elif info['cid'] != -1:
        CID = info['cid']
    else:
        return JsonResponse({'message': 'error'})
    user_list = []
    list1 = models.Message.objects.filter(SID = CID)
    list2 = models.Message.objects.filter(RID = CID)
    for l in list1:
        user_list.append(l.RID)
    for l in list2:
        user_list.append(l.SID)
    return JsonResponse({'message': list(set(user_list))})