from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string 
from .. import models
from chatterbot import ChatBot

def enterprise_signup_helper(info):
    #检查email是否已经存在
    email = info['email']
    if len(models.Enterprise.objects.filter(email=email)) > 0:
        return JsonResponse({
            'message': '该邮箱已注册'
            })
    name = info['name']
    ri = 'http://www.jb51.net/images/logo.gif'
    rn = '小机'
    m = hashlib.md5()
    m.update(str(int(time.time())).encode('utf8'))
    eid = m.hexdigest()
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    info['password'] += salt
    m = hashlib.md5()
    m.update(info['password'].encode('utf8'))
    password = m.hexdigest()
    try:
        models.Enterprise.objects.create(EID = eid, email = email, password = password, name = name, robot_icon = ri, robot_name = rn, salt = salt)
        return JsonResponse({
            'message': '注册成功'
            })
    except Exception:
        return JsonResponse({
            'message': '注册失败'
            })

@ensure_csrf_cookie
def enterprise_signup(request):
    """
        企业注册
    """
    info = json.loads(request.body.decode('utf8'))
    return enterprise_signup_helper(info)
    
@ensure_csrf_cookie
def enterprise_login_helper(info):
    try:
        email = info['email']
        password = info['password']
        right = models.Enterprise.objects.get(email = email)
        m = hashlib.md5()
        password += right.salt
        m.update(password.encode('utf8'))
        if m.hexdigest() == right.password:
            #成功
            return (1, right.EID)
        else:
            #密码错误
            return (0, '密码错误')
    except Exception:
        #账号错误
        return (-1, '账号错误')

@ensure_csrf_cookie
def enterprise_login(request):
    """
        企业登陆
    """
    info = json.loads(request.body.decode('utf8'))
    code = enterprise_login_helper(info)
    if code[0] == 0 or code[0] == -1:
        return JsonResponse({
            'message': code[1]
            })
    else:
        request.session['EID'] = code[1]
        return JsonResponse({
            'message': '登陆成功'
            })
