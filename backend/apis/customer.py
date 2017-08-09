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
    if hasattr(request, 'session') and 'cid' in request.session:
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
        customer = models.Customer.objects.filter(email = email)[0]
        md5 = hashlib.md5()
        password += customer.salt
        md5.update(password.encode('utf8'))
        if md5.hexdigest() == customer.password:
            if customer.state == 1:
                #成功
                models.Customer.objects.filter(email = email).update(state = 3)
                return (1, customer.CID)
            elif customer.state == 0:
                #账号未激活
                return (0, -5)
            elif customer.state == -1:
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
        request.session['cid'] = code[1]
        request.session['email'] = info['email']
        return JsonResponse({'flag': 1, 'message': ''})

@ensure_csrf_cookie
def customer_logout(request):
    """客服退出"""
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    models.Customer.objects.filter(CID = CID).update(state = 1)
    return JsonResponse({'flag': 1, 'message': ''})

@ensure_csrf_cookie
def customer_change_onlinestate(request):
    """客服改变在线状态"""
    CID = 'cid1'
    if 'eid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    customer = models.Customer.objects.filter(CID = CID)
    if customer.state == 3:
        models.Customer.objects.filter(CID = CID)[0].update(state = 2)
    elif customer.state == 2:
        models.Customer.objects.filter(CID = CID)[0].update(state = 3)
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    return JsonResponse({'flag': 1, 'message': ''})

@ensure_csrf_cookie
def customer_serviced_number(request):
    """获取客服服务过的人数"""
    CID = 'cid1'
    if 'eid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    customer = models.Customer.objects.filter(CID = CID)
    return JsonResponse({'flag': 1, 'message': customer.serviced_number})

@ensure_csrf_cookie
def customer_dialogs_oneday(request):
    """获取客服最近24小时会话数"""
    CID = 'cid1'
    if 'eid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        time1 = time.mktime(nowtime.timetuple())
        time2 = time.mktime(dialog.start_time.timetuple())
        if time1 - time2 < 60 * 60 * 24:
            total += 1
    return JsonResponse({'flag': 1, 'message': total})
