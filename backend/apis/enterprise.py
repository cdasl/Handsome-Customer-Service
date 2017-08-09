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
import datetime, time

def signup_init(info):
    """初始化注册信息"""
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
    """修改密码"""
    email = info['email']
    old_password = info['old']
    new_password = info['new']
    obj = models.Enterprise.objects.get(email = email)
    salt = obj.salt
    md5 = hashlib.md5()
    md5.update((old_password + salt).encode('utf8'))
    password = md5.hexdigest()
    if password != obj.password:
        return JsonResponse({'flag': -1, 'message': ''})
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    md5 = hashlib.md5()
    md5.update((new_password + salt).encode('utf8'))
    password = md5.hexdigest()
    try:
        obj.salt = salt
        obj.password = password
        obj.save()
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -2, 'message': ''})

@ensure_csrf_cookie
def enterprise_signup(request):
    """企业注册"""
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    #检查email是否已经存在
    if len(models.Enterprise.objects.filter(email = email)) > 0:
        return JsonResponse({'flag': -3, 'message': ''})
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
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -4, 'message': ''})

def enterprise_login_helper(info):
    try:
        email = info['email']
        password = info['password']
        enterprise = models.Enterprise.objects.get(email = email)
        md5 = hashlib.md5()
        password += enterprise.salt
        md5.update(password.encode('utf8'))
        if md5.hexdigest() == enterprise.password:
            if enterprise.state == 1:
                #成功
                return (1, enterprise.EID)
            elif enterprise.state == 0:
                #账号未激活
                return (0, -5)
            elif enterprise.state == -1:
                #账号被注销
                return (-1, -6)
        else:
            #密码错误
            return (-2, -1)
    except Exception:
        #账号错误
        return (-3, -7)

@ensure_csrf_cookie
def enterprise_login(request):
    """企业登录"""
    info = json.loads(request.body.decode('utf8'))
    code = enterprise_login_helper(info)
    if code[0] < 1:
        return JsonResponse({'flag': code[1], 'message': ''})
    else:
        request.session['eid'] = code[1]
        request.session['email'] = info['email']
        return JsonResponse({'flag': 1, 'message': ''})

@csrf_exempt
def enterprise_active(request):
    """企业激活"""
    info = json.loads(request.body.decode("utf8"))
    active_code = info['active_code']
    decrypt_str = helper.decrypt(9, active_code)
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    enterprise = models.Enterprise.objects.filter(email = email)
    if len(enterprise) == 0:
        #链接无效
        return JsonResponse({'flag': -8, 'message': ''})
    create_date = time.mktime(time.strptime(decrypt_data[1], "%Y-%m-%d"))
    time_lag = time.time() - create_date
    if time_lag > 7 * 24 * 60 * 60:
        #链接过期
        return JsonResponse({'flag': -9, 'message': ''})
    if enterprise[0].state == 1:
        #已经激活
        return JsonResponse({'flag': 1, 'message': ''})
    models.Enterprise.objects.filter(email = email)[0].update(state = 1)
    #成功
    return JsonResponse({'flag': 1, 'message': ''})

@ensure_csrf_cookie
def enterprise_invite(request):
    """邀请客服"""
    EID = 'test_eid'
    info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    email = info['email']
    if len(models.Customer.objects.filter(email = email)) > 0:
        return JsonResponse({'flag': -10, 'message': ''})
    try:
        set_customer_message(email, EID)
        active_code = helper.get_active_code(email)
        mySubject = messages.customer_active_subject()
        myMessage = messages.customer_active_message(
            'http:/127.0.0.1:8000%s' % ('/customer_active/' + active_code))
        helper.send_active_email(email, mySubject, myMessage)
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -11, 'message': ''})

def set_customer_message(email, EID):
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    CID = md5.hexdigest()
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    password = '12345678'
    icon = 'demo.png'
    name = '张三'
    last_login = timezone.now()
    models.Customer.objects.create(CID = CID, EID = EID, email = email, password = password, 
        icon = icon, name = name, last_login = last_login, salt = salt)

@ensure_csrf_cookie
def reset_password_request(request):
    """重置密码请求"""
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    valid_enterprise = models.Enterprise.objects.filter(email = email)
    vaild_customer = models.Customer.objects.filter(email = email)
    if len(valid_enterprise) == 0 and len(vaild_customer) == 0:
        return JsonResponse({'flag': -8, 'message': ''})
    active_code = helper.get_active_code(email)
    url = 'http://127.0.0.1:8000/password_reset/%s' % (active_code)
    mySubject = u"重置密码"
    myMessage = messages.reset_password_message(url)
    try:
        helper.send_active_email(email, mySubject, myMessage)
        if len(valid_enterprise) > 0:
            return JsonResponse({'flag': 1, 'message': 'enterprise_reset'})
        return JsonResponse({'flag': 1, 'message': 'customer_reset'})
    except Exception:
        return JsonResponse({'flag': -12, 'message': ''})

@ensure_csrf_cookie
def reset_password(request):
    """重置密码，前端发送激活码，新密码"""
    info = json.loads(request.body.decode('utf8'))
    tip = helper.active_code_check(info['active_code'])
    if tip == 'invalid':
        return JsonResponse({'flag': -8, 'message': ''})
    if tip == 'expired':
        return JsonResponse({'flag': -9, 'message': ''})
    decrypt_str = helper.decrypt(9, info['active_code'])
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    password_salt = helper.password_add_salt(info['password'])
    try:
        enterprise = models.Enterprise.objects.filter(email = email)
        if len(enterprise) > 0:
            models.Enterprise.objects.filter(email = email)[0].update(password = password_salt['password'], 
                salt = password_salt['salt'])
        else:
            customer = models.Customer.objects.filter(email = email)
            models.Customer.objects.filter(email = email)[0].update(password = password, salt = salt)
        return JsonResponse({'flag': 1, 'message': 'reset'})
    except Exception:
        return JsonResponse({'flag': -12, 'message': ''})

@ensure_csrf_cookie
def reset_customer_state(request):
    """改变客服激活与否的状态"""
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'flag': -13, 'message': ''})
    customer_name = customer[0].name
    try:
        if customer[0].state > 0:
            models.Customer.objects.filter(CID = CID)[0].update(state = -1)
            return JsonResponse({'flag': 1, 'message': 'logoff success'})
        elif customer[0].state == -1:
            models.Customer.objects.filter(CID = CID)[0].update(state = 1)
            return JsonResponse({'flag': 1, 'message': 'activate success'})
    except Exception:
        return JsonResponse({'flag': -14, 'message': ''})

@ensure_csrf_cookie
def enterprise_get_customers(request):
    """获取客服人员列表"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    customer_list = []
    customers = models.Customer.objects.filter(EID = EID)
    for customer in customers:
        customer_list.append({'cid': customer.CID, 'name': customer.name, 'email': customer.email,
            'state': customer.state, 'service_number': customer.service_number, 'serviced_number': customer.serviced_number})
    #return JsonResponse({'message': customer_list})
    return JsonResponse({'flag': 1, 'message': customer_list})
    
@ensure_csrf_cookie
def inquire_customer_info(request):
    """根据客服ID查询客服信息"""
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'flag': -13, 'message': ''})
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
        return JsonResponse({'flag': 1, 'message': info})
    except Exception:
        return JsonResponse({'flag': -15, 'message': ''})

@ensure_csrf_cookie
def enterprise_online_customers(request):
    """获取在线客服人员列表"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    online_list = []
    customers = models.Customer.objects.filter(EID = EID, state = 2)
    for customer in customers:
        online_list.append({'cid': customer.CID, 'name': customer.name})
    return JsonResponse({'flag': 1, 'message': online_list})

@ensure_csrf_cookie
def enterprise_total_servicetime(request):
    """获取企业总的服务时间，返回的是分钟"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total = 0
    times = models.Dialog.objects.filter(EID = EID)
    for t in times:
        total += (t.end_time - t.start_time).seconds
    total /= 60
    return JsonResponse({'flag': 1, 'message': total})

@ensure_csrf_cookie
def enterprise_total_messages(request):
    """获取企业发送的总消息数"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total = 0
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        total += len(models.Message.objects.filter(DID = dialog.DID))
    return JsonResponse({'flag': 1, 'message': total})

@ensure_csrf_cookie
def enterprise_total_dialogs(request):
    """获取企业发送的总会话数"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    return JsonResponse({'flag': 1, 'message': len(models.Dialog.objects.filter(EID = EID))})

@ensure_csrf_cookie
def enterprise_dialogs(request):
    """获取企业全部会话列表"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    dialogs_list = []
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        dialogs_list.append({'did': dialog.DID, 'start_time': dialog.start_time, 'end_time': dialog.end_time})
    return JsonResponse({'flag': 1, 'message': dialogs_list})

@ensure_csrf_cookie
def enterprise_dialog_messages(request):
    """获取企业某个会话的内容"""
    info = json.loads(request.body.decode('utf8'))
    DID = info['did']
    #检查是否存在该did
    dialog = models.Message.objects.filter(DID = DID)
    if len(dialog) == 0:
        return JsonResponse({'flag': -16, 'message': ''})
    messages_list = []    
    messages = models.Message.objects.filter(DID = DID)
    for message in messages:
        messages_list.append({'mid': message.MID, 'sid': message.SID, 'content': message.content, 'rid': message.RID, 'date': message.date})
    return JsonResponse({'flag': 1, 'message': messages_list})

@ensure_csrf_cookie
def messages_between_chatters(request):
    """根据聊天者ID获取聊天内容"""
    info = json.loads(request.body.decode('utf8'))
    SID = info['sid']
    RID = info['rid']
    #检查是否存在该sid
    sid_mes = models.Message.objects.filter(SID = SID)
    if len(sid_mes) == 0:
        return JsonResponse({'flag': -17, 'message': ''})
    #检查是否存在该rid
    rid_mes = models.Message.objects.filter(RID = RID)
    if len(rid_mes) == 0:
        return JsonResponse({'flag': -18, 'message': ''})
    messages_list = []    
    messages = models.Message.objects.filter(SID=SID, RID=RID)
    for message in messages:
        messages_list.append({'mid': message.MID, 'sid': message.SID, 'content': message.content, 'rid': message.RID, 'date': message.date})
    return JsonResponse({'flag': 1, 'message': messages_list})

@ensure_csrf_cookie
def enterprise_avgtime_dialogs(request):
    """获取客服会话平均时间"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    totaltime = 0
    times = models.Dialog.objects.filter(EID = EID)
    for t in times:
        totaltime += (t.end_time - t.start_time).seconds
    totaltime /= 60
    totaldialogs = len(models.Dialog.objects.filter(EID = EID))
    avgtime = round(totaltime / totaldialogs, 2)
    return JsonResponse({'flag': 1, 'message': avgtime})

@ensure_csrf_cookie
def enterprise_set_robot_message(request):
    """设置企业机器人名字，头像"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    #enterprise = models.Enterprise.objects.filter(EID = EID, state = 1)
    try:
        models.Enterprise.objects.filter(EID = EID, state = 1)[0].update(robot_name = info['robot_name'])
        models.Enterprise.objects.filter(EID = EID, state = 1)[0].update(robot_icon = info['robot_icon'])
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -12, 'message': ''})

@ensure_csrf_cookie
def enterprise_avgmes_dialogs(request):
    """获取企业会话的平均消息数"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total_messages = 0
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        total_messages += len(models.Message.objects.filter(DID = dialog.DID))
    total_dialogs = len(models.Dialog.objects.filter(EID = EID))
    avgmes = round(total_messages / total_dialogs, 2)
    return JsonResponse({'flag': 1, 'message': avgmes})

@ensure_csrf_cookie
def enterprise_set_chatbox_type(request):
    """设置聊天窗口弹出方式"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    #enterprise = models.Enterprise.objects.filter(EID = EID, state = 1)
    try:
        models.Enterprise.objects.filter(EID = EID, state = 1)[0].update(chatbox_type = info['chatbox_type'])
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -12, 'message': ''})

@ensure_csrf_cookie
def enterprise_setuser_message(request):
    """企业将用户信息传给系统"""
    info =  {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    try:
        models.User.objects.create(UID = info['uid'])
        return JsonResponse({'flag': 1, 'message': ''})
    except Exception:
        return JsonResponse({'flag': -12, 'message': ''})

@ensure_csrf_cookie
def enterprise_message_number(request):
    """获取企业近24小时的消息数"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total = 0
    nowtime = timezone.now()
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        for message in models.Message.objects.filter(DID = dialog.DID):
            #获取当前时间距离1970.1.1的秒数
            time1 = time.mktime(nowtime.timetuple())
            time2 = time.mktime(message.date.timetuple())
            if time1 - time2 < 60 * 60 * 24:
                total += 1
    return JsonResponse({'flag': 1, 'message': total})

@ensure_csrf_cookie
def enterprise_serviced_number(request):
    """获取所有客服最近24小时服务的总人数"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    nowtime = timezone.now()
    serviced = []
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        for message in models.Message.objects.filter(DID = dialog.DID):
            #获取当前时间距离1970.1.1的秒数
            time1 = time.mktime(nowtime.timetuple())
            time2 = time.mktime(message.date.timetuple())
            if time1 - time2 < 60 * 60 * 24:
                serviced.append(message.RID)
    return JsonResponse({'flag': 1, 'message': len(list(set(serviced)))})

@ensure_csrf_cookie
def enterprise_dialogs_oneday(request):
    """获取企业所有客服24小时内会话数"""
    info = {'eid': -1}
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
           EID = request.session['eid']
    elif info['eid'] != -1:
        EID = info['eid']
    else:
        return JsonResponse({'flag': -12, 'message': ''})
    total = 0
    nowtime = timezone.now()
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        #获取当前时间距离1970.1.1的秒数
        time1 = time.mktime(nowtime.timetuple())
        time2 = time.mktime(dialog.start_time.timetuple())
        if time1 - time2 < 60 * 60 * 24:
            total += 1
    return JsonResponse({'flag': 1, 'message': total})
