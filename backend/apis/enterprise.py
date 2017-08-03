from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string 
from .. import models
from chatterbot import ChatBot

from . import helper
from . import messages

def signup_init(info):
    m = hashlib.md5()
    m.update(str(int(time.time())).encode('utf8'))
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    info['password'] += salt
    n = hashlib.md5()
    n.update(info['password'].encode('utf8'))
    password = n.hexdigest()
    return {'ri': 'http://www.jb51.net/images/logo.gif',
            'rn': u'小机',
            'eid': m.hexdigest(),
            'salt': salt,
            'email': info['email'],
            'name': info['name'],
            'password': password
            }

def enterprise_changepassword(info):
    """
        修改密码
    """
    email = info['email']
    old_password = info['old']
    new_password = info['new']
    obj = models.Enterprise.objects.get(email = email)
    salt = obj.salt
    m = hashlib.md5()
    m.update((old_password+salt).encode('utf8'))
    password = m.hexdigest()
    if password != obj.password:
        return JsonResponse({
            'message': '密码不正确'
            })
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    m = hashlib.md5()
    m.update((new_password + salt).encode('utf8'))
    password = m.hexdigest()
    try:
        obj.salt = salt
        obj.password = password
        obj.save()
        return JsonResponse({
            'message': '修改成功'
            })
    except Exception:
        return JsonResponse({
            'message': '修改失败'
            })

@ensure_csrf_cookie
def enterprise_signup(request):
    """
        企业注册
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    #检查email是否已经存在
    if len(models.Enterprise.objects.filter(email = email)) > 0:
        return JsonResponse({
            'message': '该邮箱已注册'
            })
    info_dict = signup_init(info)
    try:
        active_code = helper.get_active_code(email)
        mySubject = messages.enterprise_active_subject
        myMessage = messages.enterprise_active_message('http:/127.0.0.1:8000%s' % ('/enterprise_active/' + active_code))
        helper.send_active_email(email, active_code, mySubject, myMessage)
        models.Enterprise.objects.create(EID=info_dict['eid'], email=email, password=info_dict['password'], 
                                         name=info_dict['name'], robot_icon=info_dict['ri'], 
                                         robot_name=info_dict['rn'], salt=info_dict['salt'])
        return JsonResponse({
            'message': '注册成功，请前往邮箱点击链接'
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
            'message': '账号错误'
            })

def enterprise_active(request):
    info = json.loads(request.body.decode("utf8"))
    active_code = info['active_code']
    decrypt_str = helper.decrypt(9,active_code) # 9 is key to decrypt
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    enterprise = models.Enterprise.objects.filter(email=email)
    if len(enterprise) == 0:
        return JsonResponse({'message': 'invalid'})#链接无效
    create_date = time.mktime(time.strptime(decrypt_data[1], "%Y-%m-%d"))
    time_lag = time.time() - create_date
    if time_lag > 7*24*60*60:
        return JsonResponse({'message': 'expired'})#链接过期
    if enterprise[0].state == 1:
        return JsonResponse({'message': 'succeeded'})#已经激活
    enterprise.update(state=1)
    return JsonResponse({'message': 'success'})#成功