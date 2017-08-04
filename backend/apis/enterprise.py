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
    md5.update((old_password + salt).encode('utf8'))
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
        myMessage = messages.enterprise_active_message(
            'http:/127.0.0.1:8000%s' % ('/enterprise_active/' + active_code))
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
        request.session['email'] = info['email']
        return JsonResponse({'message': 'Login Success!'})

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
    enterprise = models.Enterprise.objects.filter(email =   email)
    if len(enterprise) == 0:
        #链接无效
        return JsonResponse({'message': 'invalid'})
    create_date = time.mktime(time.strptime(decrypt_data[1], "%Y-%m-%d"))
    time_lag = time.time() - create_date
    if time_lag > 7 * 24 * 60 * 60:
        #链接过期
        return JsonResponse({'message': 'expired'})
    if enterprise[0].state == 1:
        #已经激活
        return JsonResponse({'message': 'succeeded'})
    enterprise.update(state = 1)
    #成功
    return JsonResponse({'message': 'success'})

@ensure_csrf_cookie
def enterprise_invite(request):
    """
        邀请客服
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    if len(models.Customer.objects.filter(email = email)) > 0:
        return JsonResponse({'message': 'the mailbox has been registered'})
    EID = request.session['eid']
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    CID = md5.hexdigest()
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    password = '12345678'
    icon = 'demo.png'
    name = '张三'
    last_login = date.today()
    try:
        models.Customer.objects.create(CID = CID, EID = EID, email = email, password = password,
                                       icon = icon, name = name, last_login = last_login, salt = salt)
        active_code = helper.get_active_code(email)
        mySubject = messages.customer_active_subject
        myMessage = messages.customer_active_message(
            'http:/127.0.0.1:8000%s' % ('/customer_active/' + active_code))
        helper.send_active_email(email, active_code, mySubject, myMessage)
        return JsonResponse({'message': 'invite successfully'})
    except Exception:
        return JsonResponse({'message': 'invite failure'})

@ensure_csrf_cookie
def reset_password_request(request):
    """
        重置密码请求
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    valid_enterprise = models.Enterprise.objects.filter(email = email)
    vaild_customer = models.Customer.objects.filter(email = email)
    if len(valid_enterprise) == 0 and len(vaild_customer) == 0:
        return JsonResponse({'message': 'invalid'})
    active_code = helper.get_active_code(email)
    url = 'http://127.0.0.1:8000/password_reset/%s' % (active_code)
    mySubject = u"重置密码"
    myMessage = messages.reset_password_message(url)
    try:
        helper.send_active_email(email, mySubject, myMessage)
        if len(valid_enterprise) > 0:
            return JsonResponse({'message': 'enterprise_reset'})
        return JsonResponse({'message': 'customer_reset'})
    except Exception:
        return JsonResponse({'message': 'error'})

@ensure_csrf_cookie
def reset_password(request):
    '''
        重置密码，前端发送激活码，新密码，激活者
    '''
    info = json.loads(request.body.decode('utf8'))
    helper.active_code_check(info['active_code'])
    decrypt_str = helper.decrypt(9, info['active_code'])
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    password_salt = helper.password_add_salt(info['password'])
    password = password_salt['password']
    salt = password_salt['salt']
    try:
        if info['who'] == 'enterprise_reset':
            enterprise = models.Enterprise.objects.filter(email = email)
            enterprise.update(password = password, salt = salt)
        else:
            customer = models.Customer.objects.filter(email = email)
            customer.update(password = password, salt = salt)
        return JsonResponse({'message': 'reset'})
    except Exception:
        return JsonResponse({'message': 'error'})

@ensure_csrf_cookie
def enterprise_logoff_customer(request):
    """
        注销客服
    """
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'message': 'not exist this customer'})
    customer_name = customer[0].name
    try:
        models.Customer.objects.filter(CID = CID).update(state = -1)
        return JsonResponse({'message': 'log off ' + customer_name + ' successfully'})
    except Exception:
        return JsonResponse({
            'message': 'fail to log off ' + customer_name
            })

@ensure_csrf_cookie
def enterprise_get_customers(request):
    """
        获取客服人员列表
    """
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and hasattr(request.session, 'eid'):
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'message': 'error'})
    customer_list = []
    customers = models.Customer.objects.filter(EID = EID)
    for customer in customers:
        customer_list.append({'cid': customer.CID, 'name': customer.name, 'email': customer.email,
            'state': customer.state, 'service_number': customer.service_number, 'serviced_number': customer.serviced_number})
    return JsonResponse({'message': customer_list})
    
@ensure_csrf_cookie
def inquire_customer_info(request):
    """
        根据客服ID查询客服信息
    """
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'message': 'not exist this customer'})
    info = {
        'name': customer[0].name,
        'EID': customer[0].EID,
        'email': customer[0].email,
        'icon': customer[0].icon,
        'state': customer[0].state,
        'service_number': customer[0].service_number,
        'serviced_number': customer[0].serviced_number,
        'last_login': customer[0].last_login
        }
    try:
        return JsonResponse({'message': info})
    except Exception:
        return JsonResponse({'message': 'fail to inquire infomation of ' + CID})

@ensure_csrf_cookie
def enterprise_online_customers(request):
    """
        获取在线客服人员列表
    """
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and hasattr(request.session, 'eid'):
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'message': 'error'})
    online_list = []
    customers = models.Customer.objects.filter(EID = EID, state = 2)
    for customer in customers:
        online_list.append({'cid': customer.CID, 'name': customer.name})
    return JsonResponse({'message': online_list})

@ensure_csrf_cookie
def enterprise_total_servicetime(request):
    """
        获取企业总的服务时间，返回的是分钟
    """
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and hasattr(request.session, 'eid'):
           EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'message': 'error'})
    total = 0
    times = models.Dialog.objects.filter(EID = EID)
    for t in times:
        total += (t.end_time - t.start_time).seconds
    total /= 60
    return JsonResponse({'message': total})

@ensure_csrf_cookie
def enterprise_total_messages(request):
    """
        获取企业发送的总消息数
    """
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and hasattr(request.session, 'eid'):
           EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'message': 'error'})
    total = 0
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        total += len(models.Message.objects.filter(DID = dialog.DID))
    return JsonResponse({'message': total})