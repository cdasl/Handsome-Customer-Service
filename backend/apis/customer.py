from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string
from .. import models, tests, const_table
from chatterbot import ChatBot
from . import helper, messages
import django.utils.timezone as timezone
import datetime, time

def jrToJson(jr):
    """将JsonResponse对象转为Json对象"""
    return json.loads(jr.content.decode('utf8'))

@ensure_csrf_cookie
def customer_chatted(request):
    """
    获取与某位客服聊过天所有用户\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**: 包含成功/失败消息和与某位客服聊过天所有用户列表的JsonResponse
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
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    user_list = []
    list1 = models.Message.objects.filter(SID = CID)
    list2 = models.Message.objects.filter(RID = CID)
    for l in list1:
        user_list.append(l.RID)
    for l in list2:
        user_list.append(l.SID)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': list(set(user_list))})

def customer_login_helper(info):
    try:
        email = info['email']
        password = info['password']
        customer = models.Customer.objects.filter(email = email)[0]
        md5 = hashlib.md5()
        password += customer.salt
        md5.update(password.encode('utf8'))
        if md5.hexdigest() == customer.password:
            if customer.state == 1  or customer.state == 2:
                #成功
                models.Customer.objects.filter(email = email).update(state = 2)
                return (1, customer.CID)
            elif customer.state == 0:
                #账号未激活
                return (0, const_table.const.ACCOUNT_NOT_ACTIVETED)
            elif customer.state == -1:
                #账号被注销
                return (-1, const_table.const.ACCOUNT_LOGGED_OFF)
        else:
            #密码错误
            return (-2, const_table.const.WRONG_PASSWORD)
    except Exception:
        #账号错误
        return (-3, const_table.const.WRONG_ACCOUNT)

@ensure_csrf_cookie
def customer_login(request):
    """
    客服登录\n
    * **request** - 前端发送的请求,包含邮箱和密码\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    info = json.loads(request.body.decode('utf8'))
    code = customer_login_helper(info)
    if code[0] < 1:
        return JsonResponse({'flag': code[1]})
    else:
        request.session['cid'] = code[1]
        request.session['email'] = info['email']
        models.Customer.objects.filter(CID = code[1]).update(last_login = datetime.datetime.now())
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def customer_logout(request):
    """
    客服退出\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    models.Customer.objects.filter(CID = CID).update(state = 1, service_number = 0)
    del request.session['cid']
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def customer_get_info(request):
    """
    客服获取自己的个人信息\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息和客服个人信息的JsonResponse
    """
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    customer = models.Customer.objects.get(CID = CID)
    info = {'cid': customer.CID, 'eid': customer.EID, 'email': customer.email, 'state': customer.state, 
    'name': customer.name, 'serviced_number': customer.serviced_number, 'service_number': customer.service_number, 
    'last_login': customer.last_login, 'icon': customer.icon}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': info})

@ensure_csrf_cookie
def customer_get_id(request):
    """
    客服获取自己的CID、EID和头像\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息和客服自己的CID、EID和头像的JsonResponse
    """
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    customer = models.Customer.objects.get(CID = CID)
    id_list = {'cid': customer.CID, 'eid': customer.EID, 'icon': customer.icon}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': id_list})

@ensure_csrf_cookie
def customer_change_onlinestate(request):
    """
    客服改变在线状态\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    customer = models.Customer.objects.filter(CID = CID)[0]
    if customer.state == 3:
        models.Customer.objects.filter(CID = CID).update(state = 2)
    elif customer.state == 2:
        models.Customer.objects.filter(CID = CID).update(state = 3)
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

def customer_serviced_number(CID):
    """
    获取客服服务过的人数\n
    * **CID** - 客服的id\n
    **返回值**:当前客服服务过的人数
    """
    customer = models.Customer.objects.filter(CID = CID)
    return customer[0].serviced_number

def customer_dialogs_oneday(CID):
    """
    获取客服最近24小时会话数\n
    * **CID** - 客服的id\n
    **返回值**:当前客服最近24小时会话数
    """
    total = 0
    nowtime = datetime.datetime.now()
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        time1 = time.mktime(nowtime.timetuple())
        time2 = time.mktime(dialog.start_time.timetuple())
        if time1 - time2 < 60 * 60 * 24:
            total += 1
    return total

def customer_total_servicedtime(CID):
    """
    返回客服总的服务时间(分钟)\n
    * **CID** - 客服的id\n
    **返回值**:当前客服总服务时间
    """
    totaltime = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        totaltime += (dialog.end_time - dialog.start_time).seconds
    totaltime = round(totaltime / 60, 2)
    return totaltime

def customer_total_messages(CID):
    """
    返回客服发送总的消息数\n
    * **CID** - 客服的id\n
    **返回值**:当前客服发送的总消息数
    """
    total = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        for message in models.Message.objects.filter(DID = dialog.DID):
            total += 1
    return total

def customer_total_dialogs(CID):
    """
    获取客服总会话数\n
    * **CID** - 客服的id\n
    **返回值**:当前客服总会话数
    """
    total = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    total = len(dialogs)
    return total

def customer_avgtime_dialogs(CID):
    """
    获取客服会话平均时间\n
    * **CID** - 客服的id\n
    **返回值**:当前客服会话的平均时间
    """
    totaltime = jrToJson(customer_total_servicedtime(CID))['message']
    total = jrToJson(customer_total_dialogs(CID))['message']
    if total == 0:
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 0})
    avgtime = round(totaltime / total, 2)
    return avgtime

def customer_avgmes_dialogs(CID):
    """
    获取客服平均消息数\n
    * **CID** - 客服的id\n
    **返回值**:当前客服平均消息数
    """
    totalmessage = 0
    totaldialog = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    totaldialog = len(dialogs)
    for dialog in dialogs:
        messages = models.Message.objects.filter(DID = dialog.DID)
        totalmessage += len(messages)
    if totaldialog == 0:
        return 0
    else:
        avgmes = round(totalmessage / totaldialog, 2)
        return avgmes

@ensure_csrf_cookie
def customer_dialogs(request):
    """
    获取客服所有会话列表\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    dialogs_list = []
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        dialogs_list.append({'cid': dialog.CID, 'uid': dialog.UID, 'start_time': dialog.start_time, 
            'end_time': dialog.end_time, 'did': dialog.DID})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': dialogs_list})

@ensure_csrf_cookie
def customer_dialog_messages(request):
    """
    获取客服某个会话内容\n
    * **request** - 前端发送的请求, session中有cid\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    info = json.loads(request.body.decode('utf8'))
    if 'cid' in request.session:
        CID = request.session['cid']
    DID = info['did']
    dialog = models.Message.objects.filter(DID = DID)
    if len(dialog) == 0:
        return JsonResponse({'flag': const_table.const.DIALOGID_NOT_EXIST})
    messages_list = []    
    messages = models.Message.objects.filter(DID = DID).order_by('date')
    for message in messages:
        if message.SID == CID or message.SID == 'robot':
            is_customer = True
        else:
            is_customer = False
        messages_list.append({'mid': message.MID, 'isCustomer': is_customer, 'content': message.content, 'date': message.date})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': messages_list})

@ensure_csrf_cookie
def reset_password_request(request):
    """
    找回密码请求\n
    * **request** - 前端发送的请求，包含email\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    valid_enterprise = models.Enterprise.objects.filter(email = email)
    vaild_customer = models.Customer.objects.filter(email = email)
    if len(valid_enterprise) == 0 and len(vaild_customer) == 0:
        return JsonResponse({'flag': const_table.const.INVALID})
    active_code = helper.get_active_code(email)
    url = 'http://127.0.0.1:8000/password_reset/%s' % (active_code)
    mySubject = u"重置密码"
    myMessage = messages.reset_password_message(url)
    try:
        helper.send_active_email(email, mySubject, myMessage)
        if len(valid_enterprise) > 0:
            return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'enterprise_reset'})
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'customer_reset'})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR, 'message': ''})

@ensure_csrf_cookie
def reset_password(request):
    """
    找回密码，前端发送激活码，新密码\n
    * **request** - 前端发送的请求,包含激活码\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    info = json.loads(request.body.decode('utf8'))
    tip = helper.active_code_check(info['active_code'])
    if tip == const_table.const.INVALID:
        return JsonResponse({'flag': const_table.const.INVALID})
    if tip == const_table.const.EXPIRED:
        return JsonResponse({'flag': const_table.const.EXPIRED})
    decrypt_str = helper.decrypt(9, info['active_code'])
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    password_salt = helper.password_add_salt(info['password'])
    try:
        enterprise = models.Enterprise.objects.filter(email = email)
        if len(enterprise) > 0:
            models.Enterprise.objects.filter(email = email).update(password = password_salt['password'], 
                salt = password_salt['salt'])
        else:
            customer = models.Customer.objects.filter(email = email)
            models.Customer.objects.filter(email = email).update(password = password, salt = salt)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'reset'})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def customer_modify_icon(request):
    """
    客服修改自己的头像,昵称\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    CID = 'cid1'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    try:
        models.Customer.objects.filter(CID = CID).update(icon = info['icon'], name = info['name'])
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def customer_get_alldata(request):
    """
    返回该客服所有数据：\n
    总服务时间，总消息数，总会话数，总服务人数，\n
    今日会话数，平均会话时长，平均消息数\n
    * **request** - 前端发送的请求,session中有cid\n
    **返回值**:包含成功/失败消息和以上所有的数据的JsonResponse
    """
    CID = 'cid1'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    try:
        totaltime = customer_total_servicedtime(CID)
        totalmessage = customer_total_messages(CID)
        totaldialog = customer_total_dialogs(CID)
        totalserviced = customer_serviced_number(CID)
        todaydialog = customer_dialogs_oneday(CID)
        avgdialogtime = customer_avgtime_dialogs(CID)
        avgmessages = customer_avgmes_dialogs(CID)
        allData = {'totalTime': totaltime, 'totalMessage': totalmessage, 'totalDialog': totaldialog, 
        'totalServiced': totalserviced, 'todayDialog': todaydialog, 'avgDialogTime': avgdialogtime, 'avgMessages': avgmessages}
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': allData})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def customer_other_online(request):
    """
    获取除当前客服外其他在线客服\n
    * **request** - 前端发来的请求，session中有cid\n
    **返回值**:包含成功/失败消息和当前其他在线客服列表的JsonResponse
    """
    CID = 'cid1'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    EID = models.Customer.objects.get(CID = CID).EID
    online_list = []
    customers = models.Customer.objects.filter(EID = EID, state = 3)
    for customer in customers:
        if(customer.CID != CID):
            online_list.append({'cid': customer.CID, 'name': customer.name})
        else:
            continue
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': online_list})

@ensure_csrf_cookie
def customer_modify_password(request):
    """
    客服修改密码\n
    * **request** - 前端发送的请求，包含旧密码和新密码\n
    **返回值**:包含成功/失败消息的JsonResponse
    """
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    obj = models.Customer.objects.get(CID = CID)
    salt = obj.salt
    md5 = hashlib.md5()
    md5.update((info['old'] + salt).encode('utf8'))
    password = md5.hexdigest()
    if password != obj.password:
        return JsonResponse({'flag': const_table.const.WRONG_PASSWORD})
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    md5 = hashlib.md5()
    md5.update((info['new'] + salt).encode('utf8'))
    password = md5.hexdigest()
    try:
        models.Customer.objects.filter(CID = CID).update(salt = salt, password = password)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.FAIL_MODIFY})
