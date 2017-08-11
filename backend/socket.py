from django.shortcuts import render
import socketio
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import hashlib, time, datetime
from .models import Dialog, Message

async_mode = None
sio = socketio.Server(async_mode = async_mode)
thread = None
talker_list = {}
customer_list = {}
conversation = {}
starttime = {}

def get_mid(msg):
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
    global conversation, talker_list
    sio.emit('my response', {'data': message['data'], 'time': message['time'], 'src': message['src'], 'sid': sid}, room = message['sid'], namespace = '/test')
    conversation[sid].append({'send': talker_list[sid], 'receive': talker_list[message['sid']], 'time': message['time'], 'data': message['data']})

@sio.on('customer message', namespace = '/test')
def customer_message(sid, message):
    global conversation, talker_list
    sio.emit('my response', {'data': message['data'], 'time': message['time'], 'src': message['src']}, room = message['sid'], namespace = '/test')
    conversation[message['sid']].append({'send': talker_list[sid], 'receive': talker_list[message['sid']], 'time': message['time'], 'data': message['data']})

@sio.on('disconnect a user', namespace = '/test')
def write_message(sid,message):
    endtime = time2str()
    msglist = []
    md5 = hashlib.md5()
    md5.update((sid + message['sid'] + str(int(time.time()))).encode('utf8'))
    did = me5.hexdigest()
    for i in conversation[message['sid']]:
        mid = get_mid(i)
        msg = Message(MID = mid, SID = i['send'], RID = i['receive'], DID = did, content = i['data'], date = i['time'])
        msglist.append(msg)
    Message.objects.bulk_create(msglist)
    del conversation[message['sid']]

@sio.on('a user connected', namespace = '/test')
def user_connect(sid, message):
    global talker_list, customer_list, conversation
    talker_list[sid] = message['uid']
    num = 100
    target = None
    for customer_sid in customer_list:
        if customer_list[customer_sid] < num:
            target = customer_sid
            num = customer_list[customer_sid]
    if target == None:
        sio.emit('no customer online', {'data': 'no customer on line'}, room = sid, namespace = '/test')
    else:
        sio.emit('connect to customer', {'sid': target}, room = sid, namespace = '/test')
        sio.emit('new user', {'sid': sid}, room = target, namespace = '/test')
        customer_list[target] += 1
        conversation[sid] = []
        starttime[sid] = time2str()

@sio.on('a customer connected', namespace = '/test')
def customer_connect(sid, message):
    global talker_list, customer_list
    talker_list[sid] = message['cid']
    customer_list[sid] = 0
    sio.emit('customer connected', {'data': 'connected'}, room = sid, namespace = '/test')

@sio.on('disconnect request', namespace = '/test')
def disconnect_request(sid):
    sio.disconnect(sid, namespace = '/test')

@sio.on('disconnect', namespace = '/test')
def test_disconnect(sid):
    print('Client disconnected')