from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models, const, const_table
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from django.http import HttpResponseRedirect

def jrToJson(jr):
    '''将JsonResponse对象转为Json对象'''
    return json.loads(jr.content.decode('utf8'))

class GetCountOfDialogsTestCase(TestCase):
    '''测试获取企业总会话数Api'''
    def setUp(self):
        time1 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did4', EID = 'test_eid3', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did5', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did6', EID = 'test_eid1', start_time = time1, end_time = time1)

    def test_count_of_dialogs(self):
        EID = 'test_eid1'
        result = jrToJson(enterprise.enterprise_total_dialogs(EID))['message']
        self.assertEqual(result, 3)

class GetChattedTestCase(TestCase):
    '''测试获取与某位客服聊过天的所有用户Api'''
    def setUp(self):
        time1 = timezone.now()
        models.Message.objects.create(MID = 'test_mid1', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid2', SID = 'test_sid2', RID = 'test_sid1', DID = 'test_did1',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid3', SID = 'test_sid1', RID = 'test_rid3', DID = 'test_did3',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid4', SID = 'test_sid4', RID = 'test_rid4', DID = 'test_did2',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid5', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content', date = time1)

    def test_get_chatted(self):
        rf = RequestFactory()
        info = {'cid': 'test_sid1'}
        request = rf.post('api/cust/get_chatted/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(customer.customer_chatted(request))['message']
        self.assertEqual(set(result), set(['test_rid1', 'test_rid3', 'test_sid2']))

class DialogsListTestCase(TestCase):
    '''测试获取企业全部会话列表Api'''
    def setUp(self):
        self.stime1 = timezone.now()
        self.stime2 = timezone.now()
        self.stime3 = timezone.now()
        self.etime1 = timezone.now()
        self.etime2 = timezone.now()
        self.etime3 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = self.stime1, end_time = self.etime1)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid1', start_time = self.stime2, end_time = self.etime2)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid2', start_time = self.stime3, end_time = self.etime3)

    def test_dialogs_list(self):
        rf = RequestFactory()
        info = {}
        request = rf.post('api/enter/test_dialogs_list/')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'test_eid1'
        result = jrToJson(enterprise.enterprise_dialogs(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['did'], 'test_did1')
        self.assertEqual(result[1]['did'], 'test_did2')
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_dialogs(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class ResetPasswordTestCase(TestCase):
    '''测试重置密码API'''
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1')
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 1,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())

    def test_reset_password_requset(self):
        rf = RequestFactory()
        request = rf.post('api/reset_password/')
        #企业
        info = {'email': '654321@qq.com'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password_request(request))['message']
        self.assertEqual(result, 'enterprise_reset')
        #客服
        info = {'email': '2222@qq.com'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password_request(request))['message']
        self.assertEqual(result, 'customer_reset')
        #错误
        info = {'email': 'cmn@rgb.com'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password_request(request))['flag']
        self.assertEqual(result, const_table.const.INVALID)
    
    def test_reset_partone(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #企业 时间问题，间隔时间太长会显示过期
        info = {'active_code': 'pdmdndkdldidjeihihhckgggegfhldjdidadecjdbdecjdid', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        #密码是否修改了
        password = '11111111'
        example = models.Enterprise.objects.get(EID = 'eid1')
        password += example.salt
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        self.assertEqual(password, example.password)
        #激活码无效
        info = {'active_code': 'thisisawrongexample', 
                'password': '7dsa987d9a8s'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, const_table.const.INVALID)

    def test_reset_parttwo(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #客服 时间有问题，时间太长会显示过期
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdmd', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, const_table.const.EXPIRED)
        #激活码过期
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdid', 
                'password': '7dsa987d9a8s'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, const_table.const.EXPIRED)

class DialogMessagesTestCase(TestCase):
    '''测试获取会话内容Api'''
    def setUp(self):
        time1 = timezone.now()
        time2 = timezone.now()
        models.Message.objects.create(MID = 'test_mid1', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content1', date = time1)
        models.Message.objects.create(MID = 'test_mid2', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content2', date = time2)
        models.Message.objects.create(MID = 'test_mid3', SID = 'test_sid3', RID = 'test_rid3', DID = 'test_did2',
            content = 'test_content3', date = time1)

    def test_dialog_messages(self):
        rf = RequestFactory()
        info = {'did': 'test_did1'}
        request = rf.post('api/enter/dialog_messages/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_dialog_messages(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['mid'], 'test_mid1')
        self.assertEqual(result[0]['sid'], 'test_sid1')
        self.assertEqual(result[0]['content'], 'test_content1')
        self.assertEqual(result[0]['rid'], 'test_rid1')
        self.assertEqual(result[1]['mid'], 'test_mid2')
        self.assertEqual(result[1]['sid'], 'test_sid1')
        self.assertEqual(result[1]['content'], 'test_content2')
        self.assertEqual(result[1]['rid'], 'test_rid1')
    
class SetRobotMessageTestCase(TestCase):
    '''测试改企业机器人名字API'''
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1', state = 1)
    
    def test_set_robot_message(self):
        rf = RequestFactory()
        info = { 
                'robot_name': 'test1',
                'robot_icon': 'test2'
        }
        request = rf.post('api/enter/set_robot_name/')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'eid1'
        result = jrToJson(enterprise.enterprise_set_robot_message(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        test_case1 = models.Enterprise.objects.get(EID = 'eid1').robot_name
        self.assertEqual('test1', test_case1)
        test_case2 = models.Enterprise.objects.get(EID = 'eid1').robot_icon
        self.assertEqual('test2', test_case2)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_message(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class MessagesBetweenChattersTestCase(TestCase):
    '''测试根据聊天者ID获取聊天内容Api'''
    def setUp(self):
        time1 = timezone.now()
        time2 = timezone.now()
        models.Message.objects.create(MID = 'test_mid1', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content1', date = time1)
        models.Message.objects.create(MID = 'test_mid2', SID = 'test_sid1', RID = 'test_rid2', DID = 'test_did2',
            content = 'test_content2', date = time1)
        models.Message.objects.create(MID = 'test_mid3', SID = 'test_sid2', RID = 'test_rid1', DID = 'test_did3',
            content = 'test_content3', date = time1)
        models.Message.objects.create(MID = 'test_mid4', SID = 'test_sid1', RID = 'test_rid2', DID = 'test_did2',
            content = 'test_content4', date = time2)

    def test_messages_between_chatters(self):
        rf = RequestFactory()
        info = {
            'sid': 'test_sid1',
            'rid': 'test_rid2'
            }
        request = rf.post('api/enter/messages_between_chatters/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.messages_between_chatters(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['mid'], 'test_mid2')
        self.assertEqual(result[0]['sid'], 'test_sid1')
        self.assertEqual(result[0]['content'], 'test_content2')
        self.assertEqual(result[0]['rid'], 'test_rid2')
        self.assertEqual(result[1]['mid'], 'test_mid4')
        self.assertEqual(result[1]['sid'], 'test_sid1')
        self.assertEqual(result[1]['content'], 'test_content4')
        self.assertEqual(result[1]['rid'], 'test_rid2')

class AvgmesDialogsTestCase(TestCase):
    '''测试获取企业会话平均消息数Api'''
    def setUp(self):
        time1 = timezone.now()
        time2 = timezone.now()
        time3 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time2)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid1', start_time = time2, end_time = time3)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Message.objects.create(MID = 'test_mid1', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content1', date = time1)
        models.Message.objects.create(MID = 'test_mid2', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content2', date = time2)
        models.Message.objects.create(MID = 'test_mid3', SID = 'test_sid3', RID = 'test_rid3', DID = 'test_did2',
            content = 'test_content3', date = time2)
        models.Message.objects.create(MID = 'test_mid4', SID = 'test_sid4', RID = 'test_rid4', DID = 'test_did3',
            content = 'test_content4', date = time1)

    def test_avgmes_dialogs(self):
        EID = 'test_eid1'
        result = jrToJson(enterprise.enterprise_avgmes_dialogs(EID))['message']
        self.assertEqual(result, 1.5)

class AvgtimeDialogsTestCase(TestCase):
    '''测试获取企业会话平均时间Api'''
    def setUp(self):
        self.time1 = timezone.now()
        self.time2 = timezone.now()
        self.time3 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = self.time1, end_time = self.time2)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid1', start_time = self.time2, end_time =self. time3)

    def test_avgmes_dialogs(self):
        EID = 'test_eid1'
        result = jrToJson(enterprise.enterprise_avgtime_dialogs(EID))['message']
        result_number = (((self.time3 - self.time1) / 2).seconds) / 60
        self.assertEqual(result, result_number)