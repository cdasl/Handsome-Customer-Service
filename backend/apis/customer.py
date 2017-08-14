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
    """获取与某位客服聊过天的所有用户"""
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
            if customer.state == 1:
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
    """客服登录"""
    info = json.loads(request.body.decode('utf8'))
    code = customer_login_helper(info)
    if code[0] < 1:
        return JsonResponse({'flag': code[1]})
    else:
        request.session['cid'] = code[1]
        request.session['email'] = info['email']
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def customer_logout(request):
    """客服退出"""
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    models.Customer.objects.filter(CID = CID).update(state = 1)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def customer_get_info(request):
    """客服获取自己的个人信息"""
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    customer = models.Customer.objects.get(CID = CID)
    info = {'cid': customer.CID, 'eid': customer.EID, 'email': customer.email, 'state': customer.state, 
    'name': customer.name, 'serviced_number': customer.serviced_number, 'service_number': customer.service_number, 
    'last_login': customer.last_login}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': info})

@ensure_csrf_cookie
def customer_get_id(request):
    """客服获取自己的CID和EID"""
    CID = 'cid1'
    if 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    customer = models.Customer.objects.get(CID = CID)
    id_list = {'cid': customer.CID, 'eid': customer.EID}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': id_list})

@ensure_csrf_cookie
def customer_change_onlinestate(request):
    """客服改变在线状态"""
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
    """获取客服服务过的人数"""
    customer = models.Customer.objects.filter(CID = CID)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': customer[0].serviced_number})

def customer_dialogs_oneday(CID):
    """获取客服最近24小时会话数"""
    total = 0
    nowtime = datetime.datetime.now()
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        time1 = time.mktime(nowtime.timetuple())
        time2 = time.mktime(dialog.start_time.timetuple())
        if time1 - time2 < 60 * 60 * 24:
            total += 1
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def customer_total_servicedtime(CID):
    """返回客服总的服务时间(分钟)"""
    totaltime = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        totaltime += (dialog.end_time - dialog.start_time).seconds
    totaltime = round(totaltime / 60, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': totaltime})

def customer_total_messages(CID):
    """返回客服发送总的消息数"""
    total = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    for dialog in dialogs:
        for message in models.Message.objects.filter(DID = dialog.DID):
            total += 1
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def customer_total_dialogs(CID):
    """获取客服总会话数"""
    total = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    total = len(dialogs)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def customer_avgtime_dialogs(CID):
    """获取客服会话平均时间"""
    totaltime = jrToJson(customer_total_servicedtime(CID))['message']
    total = jrToJson(customer_total_dialogs(CID))['message']
    avgtime = round(totaltime / total, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': avgtime})

def customer_avgmes_dialogs(CID):
    """获取客服平均消息数"""
    totalmessage = 0
    totaldialog = 0
    dialogs = models.Dialog.objects.filter(CID = CID)
    totaldialog = len(dialogs)
    for dialog in dialogs:
        messages = models.Message.objects.filter(DID = dialog.DID)
        totalmessage += len(messages)
    avgmes = round(totalmessage / totaldialog, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': avgmes})

@ensure_csrf_cookie
def customer_dialogs(request):
    """获取客服所有会话列表"""
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
    """获取客服某个会话内容"""
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
    """重置密码请求"""
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
    """重置密码，前端发送激活码，新密码"""
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
    """客服修改自己的头像,昵称"""
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
    """返回该客服所有数据：总服务时间，总消息数，总会话数，总服务人数，
       今日会话数，平均会话时长，平均消息数
    """
    CID = 'cid1'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'cid' in request.session:
        CID = request.session['cid']
    else:
        return JsonResponse({'flag': const_table.const.CID_NOT_EXIST})
    try:
        totaltime = jrToJson(customer_total_servicedtime(CID))['message']
        totalmessage = jrToJson(customer_total_messages(CID))['message']
        totaldialog = jrToJson(customer_total_dialogs(CID))['message']
        totalserviced = jrToJson(customer_serviced_number(CID))['message']
        todaydialog = jrToJson(customer_dialogs_oneday(CID))['message']
        avgdialogtime = jrToJson(customer_avgtime_dialogs(CID))['message']
        avgmessages = jrToJson(customer_avgmes_dialogs(CID))['message']
        allData = {'totalTime': totaltime, 'totalMessage': totalmessage, 'totalDialog': totaldialog, 
        'totalServiced': totalserviced, 'todayDialog': todaydialog, 'avgDialogTime': avgdialogtime, 'avgMessages': avgmessages}
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': allData})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})
