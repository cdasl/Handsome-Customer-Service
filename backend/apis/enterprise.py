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

def signup_init(info):
    """
        初始化注册信息
    """
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    info['password'] += salt
    md5 = hashlib.md5()
    md5.update(info['password'].encode('utf8'))
    password = md5.hexdigest()
    return {'ri': 'http://www.jb51.net/images/logo.gif',
            'rn': u'小机',
            'eid': md5.hexdigest(),
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
    md5 = hashlib.md5()
    md5.update((old_password+salt).encode('utf8'))
    password = md5.hexdigest()
    if password != obj.password:
        return JsonResponse({'message': 'Wrong password'})
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    md5 = hashlib.md5()
    md5.update((new_password + salt).encode('utf8'))
    password = md5.hexdigest()
    try:
        obj.salt = salt
        obj.password = password
        obj.save()
        return JsonResponse({'message': 'Modified successfully'})
    except Exception:
        return JsonResponse({'message': 'Fail to modify'})

@ensure_csrf_cookie
def enterprise_signup(request):
    """
        企业注册
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    #检查email是否已经存在
    if len(models.Enterprise.objects.filter(email = email)) > 0:
        return JsonResponse({'message': 'This email has been registered'})
    info_dict = signup_init(info)
    try:
        active_code = helper.get_active_code(email)
        mySubject = messages.enterprise_active_subject()
        myMessage = messages.enterprise_active_message('http:/127.0.0.1:8000%s' % ('/enterprise_active/' + active_code))
        helper.send_active_email(email, mySubject, myMessage)
        models.Enterprise.objects.create(EID = info_dict['eid'], email = email, password = info_dict['password'], 
                                         name = info_dict['name'], robot_icon = info_dict['ri'], 
                                         robot_name = info_dict['rn'], salt = info_dict['salt'])
        return JsonResponse({'message': 'Sign up successfully, please go to check your email'})
    except Exception:
        return JsonResponse({'message': 'Fail to sign up'})

def enterprise_login_helper(info):
    try:
        email = info['email']
        password = info['password']
        right = models.Enterprise.objects.get(email = email)
        md5 = hashlib.md5()
        password += right.salt
        md5.update(password.encode('utf8'))
        if md5.hexdigest() == right.password:
            #成功
            return (1, right.EID)
        else:
            #密码错误
            return (0, 'wrong password')
    except Exception:
        #账号错误
        return (-1, 'wrong account')

@ensure_csrf_cookie
def enterprise_login(request):
    """
        企业登录
    """
    info = json.loads(request.body.decode('utf8'))
    code = enterprise_login_helper(info)
    if code[0] == 0 or code[0] == -1:
        return JsonResponse({'message': code[1]})
    else:
        request.session['eid'] = code[1]
        return JsonResponse({'message': 'wrong account'})

@ensure_csrf_cookie
def enterprise_active(request):
    """
        企业激活
    """
    info = json.loads(request.body.decode("utf8"))
    active_code = info['active_code']
    decrypt_str = helper.decrypt(9, active_code)
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    enterprise = models.Enterprise.objects.filter(email = email)
    if len(enterprise) == 0:
        #链接无效
        return JsonResponse({'message': 'invalid'})
    create_date = time.mktime(time.strptime(decrypt_data[1], "%Y-%m-%d"))
    time_lag = time.time() - create_date
    if time_lag > 7*24*60*60:
        #链接过期
        return JsonResponse({'message': 'expired'})
    if enterprise[0].state == 1:
        #已经激活
        return JsonResponse({'message': 'succeeded'})
    enterprise.update(state = 1)
    #成功
    return JsonResponse({'message': 'success'})
    