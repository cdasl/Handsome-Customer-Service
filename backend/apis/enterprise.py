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
import random

def jrToJson(jr):
    """
    将JsonResponse对象转为Json对象\n
    * **jr** - JsonResponse对象\n
    **返回值**: 对应的Json对象\n
    """
    return json.loads(jr.content.decode('utf8'))

def signup_init(info):
    """
    初始化注册信息\n
    * **info** - 含有注册信息的字典\n
    **返回值**: 填充完整的注册信息的字典\n
    """
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    info['password'] += salt
    md5 = hashlib.md5()
    md5.update(info['password'].encode('utf8'))
    password = md5.hexdigest()
    name_list = ['库', '里', '汤', '普', '森', '杜', '兰', '特', '格', '林', '科', '尔', '尼', '克', '杨', '麦', '基']
    return {'ri': 'http://www.jb51.net/images/logo.gif',
            'rn': (random.choice(name_list) + random.choice(name_list)),
            'rs': 1,
            'eid': md5.hexdigest(),
            'salt': salt,
            'email': info['email'],
            'name': info['name'],
            'password': password
            }

@ensure_csrf_cookie
def enterprise_changepassword(request):
    """
    企业修改密码\n
    * **request** - 前端发送的请求，包含旧密码和session\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    obj = models.Enterprise.objects.get(EID =EID)
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
        models.Enterprise.objects.filter(EID =EID).update(salt = salt, password = password)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.FAIL_MODIFY})

@ensure_csrf_cookie
def enterprise_signup(request):
    """
    企业注册\n
    * **request** - 前端发送的请求，包含邮箱，密码，企业名称\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    email = info['email']
    #检查email是否已经存在
    if len(models.Enterprise.objects.filter(email = email)) > 0:
        return JsonResponse({'flag': const_table.const.EMAIL_REGISTERED})
    info_dict = signup_init(info)
    try:
        active_code = helper.get_active_code(email)
        mySubject = messages.enterprise_active_subject()
        myMessage = messages.enterprise_active_message(
            'http:/127.0.0.1:8000%s' % ('/enterprise_active/' + active_code))
        helper.send_active_email(email, mySubject, myMessage)
        models.Enterprise.objects.create(EID = info_dict['eid'], email = email, password = info_dict['password'],
                                         name = info_dict['name'], robot_icon = info_dict['ri'],
                                         robot_name = info_dict['rn'], robot_state = info_dict['rs'], 
                                         salt = info_dict['salt'])
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.FAIL_SIGN_UP})

def enterprise_login_helper(info):
    """
    企业登录预处理\n
    * **info** - 包含登录信息的字典\n
    **返回值**: 包含成功/失败信息的列表\n
    """
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
                return (0, const_table.const.ACCOUNT_NOT_ACTIVETED)
            elif enterprise.state == -1:
                #账号被注销
                return (-1, const_table.const.ACCOUNT_LOGGED_OFF)
        else:
            #密码错误
            return (-2, const_table.const.WRONG_PASSWORD)
    except Exception:
        #账号错误
        return (-3, const_table.const.WRONG_ACCOUNT)

@ensure_csrf_cookie
def enterprise_login(request):
    """
    企业登录\n
    * **request** - 前端发送的请求，包含邮箱，密码\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    code = enterprise_login_helper(info)
    if code[0] < 1:
        return JsonResponse({'flag': code[1]})
    else:
        request.session['eid'] = code[1]
        request.session['email'] = info['email']
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def enterprise_logout(request):
    """
    企业退出登录\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    del request.session['eid']
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@csrf_exempt
def enterprise_active(request):
    """
    企业激活\n
    * **request** - 前端发送的请求，包含激活码\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    info = json.loads(request.body.decode("utf8"))
    active_code = info['active_code']
    decrypt_str = helper.decrypt(9, active_code)
    decrypt_data = decrypt_str.split('|')
    email = decrypt_data[0]
    enterprise = models.Enterprise.objects.filter(email = email)
    if len(enterprise) == 0:
        #链接无效
        return JsonResponse({'flag':const_table.const.INVALID})
    create_date = time.mktime(time.strptime(decrypt_data[1], "%Y-%m-%d"))
    time_lag = time.time() - create_date
    if time_lag > 7 * 24 * 60 * 60:
        #链接过期
        return JsonResponse({'flag': const_table.const.EXPIRED})
    if enterprise[0].state == 1:
        #已经激活
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    models.Enterprise.objects.filter(email = email).update(state = 1)
    #成功
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def enterprise_invite(request):
    """
    企业邀请客服加入\n
    * **request** - 前端发送的请求，包含客服的邮箱和session\n
    **返回值**: 包含成功/失败信息和客服信息的JsonResponse\n
    """
    EID = 'test_eid'
    info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    email = info['email']
    if len(models.Customer.objects.filter(email = email)) > 0:
        return JsonResponse({'flag': const_table.const.MAILBOX_REGISTERED})
    try:
        customer_info = tests.jrToJson(set_customer_message(email, EID))['message']
        active_code = helper.get_active_code(email)
        mySubject = messages.customer_active_subject()
        myMessage = messages.customer_active_message(
            'http:/127.0.0.1:8000%s' % ('/customer_active/' + active_code))
        helper.send_active_email(email, mySubject, myMessage)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': customer_info})
    except Exception:
        return JsonResponse({'flag': const_table.const.INVITE_FAILURE})

def set_customer_message(email, EID):
    """
    设置客服默认信息\n
    * **email** - 客服的邮箱\n
    * **EID** - 客服所在企业的ID\n
    **返回值**: 包含成功/失败信息和客服信息的JsonResponse\n
    """
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    CID = md5.hexdigest()
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    password = '12345678'
    password += salt
    md52 = hashlib.md5()
    md52.update(password.encode('utf8'))
    password = md52.hexdigest()
    icon = 'demo.png'
    name_list = ['库', '里', '汤', '普', '森', '杜', '兰', '特', '格', '林', '科', '尔', '尼', '克', '杨', '麦', '基']
    name = random.choice(name_list) + random.choice(name_list)
    last_login = datetime.datetime.now()
    models.Customer.objects.create(CID = CID, EID = EID, email = email, password = password, 
        icon = icon, name = name, last_login = last_login, salt = salt)
    customer_info = {'cid': CID, 'name': name, 'email': email, 'state': 0, 'service_number': 0, 'serviced_number': 0}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': customer_info})

@ensure_csrf_cookie
def reset_password_request(request):
    """
    发送重置密码的请求\n
    * **request** - 前端发送的请求，包含需要重置的企业邮箱\n
    **返回值**: 包含成功/失败信息和修改者的JsonResponse\n
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
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def reset_password(request):
    """
    重置密码\n
    * **request** - 前端发送的请求，包含激活码和新密码\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    tip = helper.active_code_check(info['active_code'])
    if tip == -8:
        return JsonResponse({'flag': const_table.const.INVALID})
    if tip == -9:
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
def reset_customer_state(request):
    """
    企业改变客服激活与否的状态\n
    * **request** - 前端发送的请求，包含客服ID\n
    **返回值**: 包含成功/失败信息和返回信息的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'flag': const_table.const.CUSTOMER_NOT_EXIST})
    customer_name = customer[0].name
    try:
        if customer[0].state > 0:
            models.Customer.objects.filter(CID = CID).update(state = -1)
            return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'logoff success'})
        elif customer[0].state == -1:
            models.Customer.objects.filter(CID = CID).update(state = 1)
            return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'activate success'})
        elif customer[0].state == 0:
            return JsonResponse({'flag': const_table.const.SUCCESS, 'message': 'not activate'})
    except Exception:
        return JsonResponse({'flag': const_table.const.FAIL_LOG_OFF})

def customer_avg_feedback(CID):
    """
    返回客服所有会话的平均评分\n
    * **CIDt** - 客服的ID\n
    **返回值**: 客服的平均评分\n
    """
    dialogs = models.Dialog.objects.filter(CID = CID)
    if(len(dialogs) == 0):
        return 0
    total_scores = 0
    for dialog in dialogs:
        total_scores += dialog.feedback
    avg_score = round(total_scores / len(dialogs), 2)
    return avg_score

@ensure_csrf_cookie
def enterprise_get_customers(request):
    """
    企业获取客服人员列表\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和客服列表信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    customer_list = []
    customers = models.Customer.objects.filter(EID = EID)
    for customer in customers:
        avg_feedback = customer_avg_feedback(customer.CID)
        customer_list.append({'cid': customer.CID, 'name': customer.name, 'email': customer.email,
            'state': customer.state, 'service_number': customer.service_number, 
            'serviced_number': customer.serviced_number, 'avg_feedback': avg_feedback})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': customer_list})
    
@ensure_csrf_cookie
def inquire_customer_info(request):
    """
    企业根据客服ID查询客服信息\n
    * **request** - 前端发送的请求，包含需要查询的客服ID\n
    **返回值**: 包含成功/失败信息和某个客服信息的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    CID = info['cid']
    #检查是否存在该客服
    customer = models.Customer.objects.filter(CID = CID)
    if len(customer) == 0:
        return JsonResponse({'flag': const_table.const.CUSTOMER_NOT_EXIST})
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
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': info})
    except Exception:
        return JsonResponse({'flag': const_tables.const.FAIL_INQUIRE_INFORMATION})

@ensure_csrf_cookie
def enterprise_online_customers(request):
    """
    企业获取在线客服人员列表\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和在线客服信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    online_list = []
    customers = models.Customer.objects.filter(EID = EID, state = 3)
    for customer in customers:
        online_list.append({'cid': customer.CID, 'name': customer.name})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': online_list})

def enterprise_total_servicetime(EID):
    """
    获取企业总的服务时间\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和服务分钟数的JsonResponse\n
    """
    total = 0
    times = models.Dialog.objects.filter(EID = EID)
    for t in times:
        total += (t.end_time - t.start_time).seconds
    total = round(total / 60, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def enterprise_total_messages(EID):
    """
    获取企业发送的总消息数\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和总消息数的JsonResponse\n
    """
    total = 0
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        total += len(models.Message.objects.filter(DID = dialog.DID))
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def enterprise_total_dialogs(EID):
    """
    获取企业发送的总会话数\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和总会话数的JsonResponse\n
    """
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': len(models.Dialog.objects.filter(EID = EID))})

@ensure_csrf_cookie
def enterprise_dialogs(request):
    """
    企业获取全部会话列表\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和会话列表信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    dialogs_list = []
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        dialogs_list.append({'did': dialog.DID, 'start_time': dialog.start_time, 'end_time': dialog.end_time,
            'uid': dialog.UID, 'cid': dialog.CID, 'feedback': dialog.feedback})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': dialogs_list})

def enterprise_total_service_number(EID):
    """
    获取企业服务过的总人数\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和服务总人数的JsonResponse\n
    """
    totalserviced = []
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        totalserviced.append(dialog.UID)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': len(list(set(totalserviced)))})

@ensure_csrf_cookie
def enterprise_dialog_messages(request):
    """
    获取企业某个会话的内容\n
    * **request** - 前端发送的请求，包含对话ID\n
    **返回值**: 包含成功/失败信息和会话内容的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    DID = info['did']
    #检查是否存在该did
    dialog = models.Message.objects.filter(DID = DID)
    if len(dialog) == 0:
        return JsonResponse({'flag': const_table.const.DIALOGID_NOT_EXIST})
    messages_list = []    
    messages = models.Message.objects.filter(DID = DID)
    for message in messages:
        messages_list.append({'mid': message.MID, 'sid': message.SID, 'content': message.content, 'rid': message.RID, 'date': message.date})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': messages_list})

@ensure_csrf_cookie
def messages_between_chatters(request):
    """
    根据聊天者ID获取聊天内容\n
    * **request** - 前端发送的请求，包含聊天双方ID\n
    **返回值**: 包含成功/失败信息和聊天内容的JsonResponse\n
    """
    info = json.loads(request.body.decode('utf8'))
    SID = info['sid']
    RID = info['rid']
    #检查是否存在该sid
    sid_mes = models.Message.objects.filter(SID = SID)
    if len(sid_mes) == 0:
        return JsonResponse({'flag': const_table.const.SID_NOT_EXIST})
    #检查是否存在该rid
    rid_mes = models.Message.objects.filter(RID = RID)
    if len(rid_mes) == 0:
        return JsonResponse({'flag': const_table.const.RID_NOT_EXIST})
    messages_list = []    
    messages = models.Message.objects.filter(SID=SID, RID=RID)
    for message in messages:
        messages_list.append({'mid': message.MID, 'sid': message.SID, 'content': message.content, 'rid': message.RID, 'date': message.date})
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': messages_list})

def enterprise_avgtime_dialogs(EID):
    """
    获取客服平均会话时间\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和平均会话分钟数的JsonResponse\n
    """
    totaltime = 0
    times = models.Dialog.objects.filter(EID = EID)
    for t in times:
        totaltime += (t.end_time - t.start_time).seconds
    totaltime /= 60
    totaldialogs = len(models.Dialog.objects.filter(EID = EID))
    avgtime = round(totaltime / totaldialogs, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': avgtime})

@ensure_csrf_cookie
def enterprise_set_robot_message(request):
    """
    企业设置机器人名字，头像\n
    * **request** - 前端发送的请求，包含session，机器人头像和名字\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        models.Enterprise.objects.filter(EID = EID, state = 1).update(robot_name = info['robot_name'], 
            robot_icon = info['robot_icon'])
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_set_robot_state(request):
    """
    企业设置机器人状态\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    robot_state = models.Enterprise.objects.get(EID = EID).robot_state
    if robot_state == 0:
        models.Enterprise.objects.filter(EID = EID).update(robot_state = 1)
    else:
        models.Enterprise.objects.filter(EID = EID).update(robot_state = 0)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})

@ensure_csrf_cookie
def enterprise_get_robot_info(request):
    """
    企业返回机器人信息\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和机器人信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    robot_name = models.Enterprise.objects.get(EID = EID).robot_name
    robot_icon = models.Enterprise.objects.get(EID = EID).robot_icon
    robot_state = models.Enterprise.objects.get(EID = EID).robot_state
    robot_info = {'robot_name': robot_name, 'robot_icon': robot_icon, 'robot_state': robot_state}
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': robot_info})

def enterprise_avgmes_dialogs(EID):
    """
    获取企业会话的平均消息数\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和机器人信息的JsonResponse\n
    """
    total_messages = 0
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        total_messages += len(models.Message.objects.filter(DID = dialog.DID))
    total_dialogs = len(models.Dialog.objects.filter(EID = EID))
    avgmes = round(total_messages / total_dialogs, 2)
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': avgmes})

@ensure_csrf_cookie
def enterprise_set_chatbox_type(request):
    """
    企业设置聊天窗口弹出方式\n
    * **request** - 前端发送的请求，包含session和聊天窗口类型\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        models.Enterprise.objects.filter(EID = EID, state = 1).update(chatbox_type = info['chatbox_type'])
        code = 'abcdefzddhetdhsdzfsdgjhgsdxghfgggtfgchgsdzdfsdghfgdfj'
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': code})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_setuser_message(request):
    """
    企业将用户信息传给系统\n
    * **request** - 前端发送的请求，包含session和用户ID\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        models.User.objects.create(UID = info['uid'])
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_message_number_oneday(request):
    """
    获取企业近24小时各时间段的消息数\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和24小时内消息数的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    total = [0 for x in range(24)]
    nowtime = datetime.datetime.now()
    time1 = nowtime.hour
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        for message in models.Message.objects.filter(DID = dialog.DID):
            #获取当前时间距离1970.1.1的秒数
            if time.mktime(nowtime.timetuple()) - time.mktime(message.date.timetuple()) < 60 * 60 * 24:
                time2 = message.date.hour
                if time2 > time1:
                    total[time1 - time2 + 24] += 1
                else:
                    total[time1 - time2] += 1
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

@ensure_csrf_cookie
def enterprise_serviced_number_oneday(request):
    """
    所有客服24小时内各时间段服务的总人数\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和24小时内服务总人数的JsonResponse\n
    """
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    nowtime = datetime.datetime.now()
    time1 = nowtime.hour
    serviced = [[] for x in range(24)]
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        if time.mktime(nowtime.timetuple()) - time.mktime(dialog.start_time.timetuple()) < 60 * 60 * 24:
            time2 = dialog.start_time.hour
            if time1 < time2:
                serviced[time1 - time2 + 24].append(dialog.UID)
            else:
                serviced[time1 - time2].append(dialog.UID)
    for i in range(0, 24):
        serviced[i] = len(list(set(serviced[i])))
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': serviced})

@ensure_csrf_cookie
def enterprise_dialogs_oneday(request):
    """
    获取企业所有客服24小时内各时间段会话总数\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和24小时内会话总数的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    total = [0 for x in range(24)]
    nowtime = datetime.datetime.now()
    time1 = nowtime.hour
    dialogs = models.Dialog.objects.filter(EID = EID)
    for dialog in dialogs:
        if time.mktime(nowtime.timetuple()) - time.mktime(dialog.start_time.timetuple()) < 60 * 60 * 24:
            time2 = dialog.start_time.hour
            if time1 < time2:
                total[time1 - time2 + 24] += 1
            else:
                total[time1 - time2] += 1
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

def enterprise_dialogs_total_oneday(EID):
    """
    获取企业最近24小时会话总数\n
    * **EID** - 企业ID\n
    **返回值**: 包含成功/失败信息和24小时会话总数的JsonResponse\n
    """
    total = 0
    nowtime = datetime.datetime.now()
    dialogs = models.Dialog.objects.filter(EID = EID)
    time1 = time.mktime(nowtime.timetuple())
    for dialog in dialogs:
        time2 = time.mktime(dialog.start_time.timetuple())
        if time1 - time2 < 60 * 60 * 24:
            total += 1
    return JsonResponse({'flag': const_table.const.SUCCESS, 'message': total})

@ensure_csrf_cookie
def enterprise_get_alldata(request):
    """
    企业获取所有数据：总服务时间，总消息数，总会话数，总服务人数，
    在线客服人数，今日会话数，平均会话时长，平均消息数\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和所有信息的JsonResponse\n
    """
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        totaltime = jrToJson(enterprise_total_servicetime(EID))['message']
        totalmessage = jrToJson(enterprise_total_messages(EID))['message']
        totaldialog = jrToJson(enterprise_total_dialogs(EID))['message']
        totalserviced = jrToJson(enterprise_total_service_number(EID))['message']
        totalonline = len(jrToJson(enterprise_online_customers(request))['message'])
        todaydialog = jrToJson(enterprise_dialogs_total_oneday(EID))['message']
        avgdialogtime = jrToJson(enterprise_avgtime_dialogs(EID))['message']
        avgmessages = jrToJson(enterprise_avgmes_dialogs(EID))['message']
        alldata = {'totalTime': totaltime, 'totalMessage': totalmessage, 'totalDialog': totaldialog, 'totalServiced': totalserviced, 
        'totalOnline': totalonline, 'todayDialog': todaydialog, 'avgDialogTime': avgdialogtime, 'avgMessages': avgmessages}
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': alldata})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_set_robot_question(request):
    """
    企业设置机器人问题，答案，类别\n
    * **request** - 前端发送的请求，包含session，问题，答案，类别\n
    **返回值**: 包含成功/失败信息和问题ID的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    question = info['question']
    answer = info['answer']
    category = info['category']
    QID = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    try:
        models.Question.objects.create(QID = QID, EID = EID, question = question, 
            answer = answer, category = category)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': QID})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_get_all_question(request):
    """
    获得企业所有问题\n
    * **request** - 前端发送的请求，包含session\n
    **返回值**: 包含成功/失败信息和所有问题的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        question_list = []
        questions = models.Question.objects.filter(EID = EID)
        for question in questions:
            question_list.append({
                'qid': question.QID, 'question': question.question, 
                'answer': question.answer, 'category': question.category
            })
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': question_list})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@csrf_exempt
def UrlValidateJudge(request):
    """
    判断request中是否含有session'\n
    * **request** - 前端发送的请求\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        enterprise = models.Enterprise.objects.get(EID = EID)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_delete_question(request):
    """
    企业删除问题\n
    * **request** - 前端发送的请求，包含session和问题ID\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        QID = info['qid']
        questions = models.Question.objects.filter(QID = QID)
        questions.delete()
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})

@ensure_csrf_cookie
def enterprise_modify_question(request):
    """企业修改问题"""
    """
    企业修改问题\n
    * **request** - 前端发送的请求，包含session，需要修改的问题ID，修改的内容\n
    **返回值**: 包含成功/失败信息的JsonResponse\n
    """
    EID = 'eid'
    if hasattr(request, 'body'):
        info = json.loads(request.body.decode('utf8'))
    if hasattr(request, 'session') and 'eid' in request.session:
        EID = request.session['eid']
    else:
        return JsonResponse({'flag': const_table.const.EID_NOT_EXIST})
    try:
        question = info['question']
        answer = info['answer']
        category = info['category']
        QID = info['qid']
        questions = models.Question.objects.filter(QID = QID)
        questions.update(question = question, answer = answer, category = category)
        return JsonResponse({'flag': const_table.const.SUCCESS, 'message': ''})
    except Exception:
        return JsonResponse({'flag': const_table.const.ERROR})
