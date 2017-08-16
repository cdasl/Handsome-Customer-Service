from django.shortcuts import render
import socketio
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import hashlib, time, datetime
from .models import Dialog, Message, Customer
from chatterbot import ChatBot
import urllib.parse

async_mode = None
sio = socketio.Server(async_mode = async_mode)
thread = None
talker_list = {}
customer_list = {}
enterprise_list = {}
conversation = {}
starttime = {}
"""
talker_list以cid或uid为key存储sid customer_list以cid为key存储uid列表 conversation以uid为key存储聊天内容
"""
chatbot = ChatBot('Ron Obvious', trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer')
chatbot.train("chatterbot.corpus.chinese")


def get_mid(msg):
    """获取消息的mid"""
    md5 = hashlib.md5()
    md5.update((msg['send'] + msg['receive'] + msg['time']).encode('utf8'))
    return md5.hexdigest()

def time2str():
    date = datetime.datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')

@csrf_exempt
def user(request):
    return render(request, 'user.html')

@sio.on('user message', namespace = '/test')
def user_message(sid, message):
    global conversation, talker_list, chatbot
    if not message['flag']:
        sio.emit('my response', {'data': message['data'], 'time': message['time'], 'src': message['src'], 'uid': message['uid']}, room = talker_list[message['cid']], namespace = '/test')
        conversation[message['uid']].append({'send': message['uid'], 'receive': message['cid'], 'time': message['time'], 'data': message['data']})
    else:
        sio.emit('my response', {'data': chatbot.get_response(urllib.parse.unquote(message['data'])).text, 'time': time2str(), 'src': '/static/img/robot_icon/1.jpg'}, room = sid, namespace = '/test')
        conversation[message['uid']].append({'send': message['uid'], 'receive': 'robot', 'time': message['time'], 'data': urllib.parse.unquote(message['data'])})
        conversation[message['uid']].append({'send': 'robot', 'receive': message['uid'], 'time': time2str(), 'data': chatbot.get_response(urllib.parse.unquote(message['data'])).text})

@sio.on('customer message', namespace = '/test')
def customer_message(sid, message):
    global conversation, talker_list
    sio.emit('my response', {'data': message['data'], 'time': message['time'], 'src': message['src']}, room = talker_list[message['uid']], namespace = '/test')
    conversation[message['uid']].append({'send': message['cid'], 'receive': message['uid'], 'time': message['time'], 'data': message['data']})

@sio.on('disconnect a user', namespace = '/test')
def write_message(sid,message):
    global starttime, conversation, talker_list
    endtime = time2str()
    msglist = []
    md5 = hashlib.md5()
    md5.update((sid + message['uid'] + str(int(time.time()))).encode('utf8'))
    did = md5.hexdigest()
    for i in conversation[message['uid']]:
        mid = get_mid(i)
        msg = Message(MID = mid, SID = i['send'], RID = i['receive'], DID = did, content = i['data'], date = i['time'])
        msglist.append(msg)
    Message.objects.bulk_create(msglist)
    Dialog.objects.create(DID = did, EID = message['eid'], start_time = starttime[message['uid']], end_time = endtime, UID = message['uid'], CID = message['cid'])
    customer = Customer.objects.get(CID = message['cid'])
    customer.serviced_number += 1
    customer.service_number -= 1
    customer.save()
    sio.emit('user disconnected', {'did': did}, room = talker_list[message['uid']], namespace = '/test')
    del conversation[message['uid']]
    del starttime[message['uid']]
    del talker_list[message['uid']]

@sio.on('user disconnect', namespace = '/test')
def user_disconnect(sid,message):
    sio.emit('user disconnected', {'uid': message['uid']}, room = talker_list[message['cid']], namespace = '/test')
    sio.disconnect(sid, namespace = '/test')

@sio.on('rate', namespace = '/test')
def rate(sid, message):
    dialog = Dialog.objects.get(DID = message['did'])
    dialog.feedback = message['rate']
    dialog.save()

@sio.on('a user connected', namespace = '/test')
def user_connect(sid, message):
    global talker_list, conversation, starttime
    if message['uid'] in talker_list:
        sio.disconnect(talker_list[message['uid']], namespace = '/test')
        sio.emit('old data', {'content': conversation[message['uid']]}, room = sid, namespace = '/test')
    else:
        conversation[message['uid']] = []
        starttime[message['uid']] = time2str()
    talker_list[message['uid']] = sid
    sio.emit('connected', {'data': 'connected'})

@sio.on('connect to customer', namespace = '/test')
def connect_customer(sid, message):
    global customer_list, conversation, talker_list, enterprise_list
    num = 100
    target = None
    if message['eid'] not in enterprise_list:
        sio.emit('no customer online', {'data': 'no customer on line'}, room = sid, namespace = '/test')
        return
    for cid in enterprise_list[message['eid']]:
        if len(customer_list[cid]) < num:
            target = cid
            num = len(customer_list[cid])
    if target == None:
        sio.emit('no customer online', {'data': 'no customer on line'}, room = sid, namespace = '/test')
    else:
        sio.emit('connected to customer', {'cid': target}, room = sid, namespace = '/test')
        sio.emit('new user', {'uid': message['uid'], 'content': conversation[message['uid']]}, room = talker_list[target], namespace = '/test')
        customer = Customer.objects.get(CID = target)
        customer.service_number += 1
        customer.save()
        customer_list[target].insert(0, message['uid'])

@sio.on('a customer connected', namespace = '/test')
def customer_connect(sid, message):
    global talker_list, customer_list, conversation, enterprise_list
    if message['cid'] in talker_list:
        sio.disconnect(talker_list[message['cid']], namespace = '/test')
        content = []
        for uid in customer_list[message['cid']]:
            content.append(conversation[uid])
        sio.emit('old data', {'list': customer_list[message['cid']], 'content': content}, room = sid, namespace = '/test')
    else:
        if message['eid'] not in enterprise_list:
            enterprise_list[message['eid']] = []
        enterprise_list[message['eid']].append(message['cid'])
        customer_list[message['cid']] = []
    talker_list[message['cid']] = sid
    sio.emit('customer connected', {'data': 'connected'}, room = sid, namespace = '/test')

@sio.on('disconnect request', namespace = '/test')
def disconnect_request(sid):
    sio.disconnect(sid, namespace = '/test')

@sio.on('disconnect', namespace = '/test')
def test_disconnect(sid):
    print('Client disconnected')