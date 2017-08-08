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
import django.utils.timezone as timezone

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
        return JsonResponse({'message': -12})
    user_list = []
    list1 = models.Message.objects.filter(SID = CID)
    list2 = models.Message.objects.filter(RID = CID)
    for l in list1:
        user_list.append(l.RID)
    for l in list2:
        user_list.append(l.SID)
    return JsonResponse({'message': list(set(user_list))})

def customer_login_helper(info):
    try:
        email = info['email']
        password = info['password']
        right = models.Customer.objects.get(email = email)
        md5 = hashlib.md5()
        password += right.salt
        md5.update(password.encode('utf8'))
        if md5.hexdigest() == right.password:
            if right.state == 1:
                #成功
                return (1, right.EID)
            elif right.state == 0:
                #账号未激活
                return (0, -5)
            elif right.state == -1:
                #账号被注销
                return (-1, -6)
        else:
            #密码错误
            return (-2, -1)
    except Exception:
        #账号错误
        return (-3, -7)

@ensure_csrf_cookie
def customer_login(request):
    """客服登录"""
    info = json.loads(request.body.decode('utf8'))
    code = customer_login_helper(info)
    if code[0] < 1:
        return JsonResponse({'flag': code[1], 'message': ''})
    else:
        request.session['eid'] = code[1]
        request.session['email'] = info['email']
        return JsonResponse({'flag': 1, 'message': ''})