#codeing: utf8
"""
    使用说明：此脚本用以在数据库中生成数据。使用方法是先打开shell，python manage.py shell, 然后将此脚本粘贴进去即可。
"""
from backend import models
import time, hashlib, datetime, random, string, math

eid = '3fb9c866c15fa98d47ee47690a6d57c0'
cids = []
uids = ['test_uid3', 'test_uid4', 'test_uid5', 'test_uid6', 'test_uid7', 'test_uid8', 'test_uid9',
        'test_uid10', 'test_uid11', 'test_uid12', 'test_uid13', 'test_uid14', 'test_uid15']
messages = ['你好', '毕竟too young', 'naive', 'excited', '谈笑风生', '比你们不知道高到哪里去了',
        '长者的身份', '董先生连任好不好啊', '吼啊', '打工是不可能打工的', '这辈子都不可能打工的',
        '超喜欢这里的', '说话又好听', '做生意嘛又不会', '人生经验']
questions = [
    {'question': '怎么看待励志书籍？', 'answer': '看再多，那都是别人的人生'},
    {'question': '＂知行合一＂到底如何理解？', 'answer': '  知道做不到，等于不知道。'},
    {'question': '如何反驳＂现实点，这个社会就是这样＂？', 'answer': ' 你是怎样，你的世界就是怎样。'},
    {'question': '有哪些道理是你读了不信，听不进去，直到你亲身经历方笃信不疑的？', 'answer': '不要低估你的能力，不要高估你的毅力。'},
    {'question': '做哪些事情可以提升生活品质？', 'answer': '定期扔东西。'},
    {'question': '什么叫见过大世面？', 'answer': '能享受最好的，也能承受最坏的。'},
    {'question': '你对自由的理解是什么？', 'answer': ' 说＂不＂的能力。'},
    {'question': '你是如何走出人生的阴霾的？', 'answer': ' 多走几步。'},
    {'question': '1+1=？', 'answer': '2'},
    {'question': '美国首都？', 'answer': '华盛顿'},
    {'question': '天王盖地虎？', 'answer': '宝塔镇河妖'},
    {'question': '草色烟光残照里?', 'answer': '无言谁会凭栏意'},
    {'question': '几度饮散歌阑？', 'answer': '香暖鸳鸯被'},
    {'question': '北大荒你不喜欢吗？', 'answer': '喜欢，它物产丰富、景色秀丽，让人流连忘返。'},
    {'question': '竺可桢走进北海公园，单是为了观赏景物吗？', 'answer': '他是来观察物候，做科学研究的。'},
    {'question': '什么叫自律？', 'answer': '自律就是自己管束自己的行为。'},
    {'question': '雪中何以赠君别？', 'answer': '惟有青青松树枝。'},
    {'question': '哪位书评客声称"南方小城市民写下的关于读书，做人的那些事"？', 'answer': '蛋挞。'},
    {'question': '信念值多少钱？', 'answer': '信念是不值钱的，它有时甚至是一个善意的欺骗。然而，你一旦坚持下去，它就会迅速升值。'},
    {'question': '什么样的青春最辉煌？', 'answer': '燃烧的青春一片光芒，很绚丽很辉煌。'},
    {'question': '什么是合作？', 'answer': '合作是互相配合。'},
    {'question': '什么是生物？', 'answer': '生物就是有生命的物体……'}
    {'question': '请问遇到这个问题怎么解决？', 'answer': '我来帮您看一下！'}
    {'question': '今天天气怎么样？', 'answer': '推荐您查看汉森客服天气预报！'}
    {'question': '这个商品可以打折吗？', 'answer': '已经是最优惠的了，亲'}
    {'question': '推荐一款比较好的产品', 'answer': '我们只生产优质产品'}
    {'question': '你说的我不太明白', 'answer': '请转接人工客服！'}
]
categories = ['人生', '常见', '技术', '产品', '售后', '运维']
names = ['库', '里', '汤', '普', '森', '杜', '兰', '特', '格', '林', '科', '尔', '尼', '克', '杨', '麦', '基']

def generate_enter():
    """随机生成一个企业账号"""
    email = 'handsome@hs.com'
    password = 'handsome'
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    md5 = hashlib.md5()
    md5.update((password + salt).encode('utf8'))
    final_password = md5.hexdigest()
    global eid
    eid = generate_str()
    models.Enterprise.objects.create(EID = eid, email = email, password = final_password,
        name = '汉森客服', robot_icon = '/static/img/robot_icon/1.jpg', state = 1,
        salt = salt, chatbox_type = 1, robot_state = 1)

def generate_name():
    """随机生成名字"""
    return random.choice(names) + random.choice(names)

def generate_str():
    """随机生成字符串"""
    time.sleep(0.01)
    md5 = hashlib.md5()
    md5.update((str(int(time.time())) + (random.choice(names)
     + random.choice(names) + random.choice(names) + random.choice(names))).encode('utf8'))
    return md5.hexdigest()

def generate_cid():
    """随机哈希生成15个客服id"""
    global cids
    for i in range(15):
        cids.append(generate_str())

def generate_email():
    """随机生成email"""
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt + '@hs.com'

def delta(num):
    """生成时间差"""
    return datetime.timedelta(minutes = num)

def generate_messages(uid, cid):
    """给两个人随机生成一段对话，并且生成一个dialog"""
    did = generate_str()
    time1 = datetime.datetime.now()
    start_time = time1 - delta(random.choice([i for i in range(24 * 60)]))
    models.Dialog.objects.create(DID = did, EID = eid, start_time = start_time, end_time = start_time + delta(random.choice([i for i in range(10)])),
        UID = uid, CID = cid, feedback = random.choice([1, 2, 3, 4, 5]))
    message_length = random.choice([i for i in range(15)])
    for i in range(message_length):
        mid = generate_str()
        content = random.choice(messages)
        sid = random.choice([uid, cid])
        rid = cid if sid == uid else uid
        date = start_time + delta(i)
        models.Message.objects.create(MID = mid, SID = sid, RID = rid, content = content, DID = did, date = date)

def generate_question():
    """给企业随机生成一些问题"""
    for item in questions:
        question = item['question']
        answer = item['answer']
        qid = generate_str()
        category = random.choice(categories)
        models.Question.objects.create(QID = qid, question = question, answer = answer, category = category, EID = eid)

def generate_customer():
    """给企业添加客服"""
    for cid in cids:
        email = generate_email()
        name = generate_name()
        icon = '/static/img/customer_icon/uh_' + str(random.choice([i + 1 for i in range(9)])) + '.gif'
        state = random.choice([i - 1 for i in range(4)])
        serviced_number = random.choice([i for i in range(100)])
        service_number = random.choice([i for i in range(10)])
        raw_password = 'password'
        salt = 'salt'
        md5 = hashlib.md5()
        md5.update((raw_password + salt).encode('utf8'))
        models.Customer.objects.create(CID = cid, EID = eid, email = email, name = name, icon = icon,
            state = state, serviced_number = serviced_number, service_number = service_number,
            salt = salt, password = md5.hexdigest(), last_login = datetime.datetime.now()
            )

def generate_dialog():
    """随机生成会话"""
    for i in range(20):
        uid = random.choice(uids)
        cid = random.choice(cids)
        generate_messages(uid, cid)

def delete_all():
    """删除数据库中所有数据"""
    models.Enterprise.objects.all().delete()
    models.Customer.objects.all().delete()
    models.Question.objects.all().delete()
    models.Message.objects.all().delete()
    models.Dialog.objects.all().delete()
    models.User.objects.all().delete()

#删除所有
delete_all()
#企业
generate_enter()
#客服
generate_cid()
generate_customer()
#问题
generate_question()
#会话
generate_dialog()