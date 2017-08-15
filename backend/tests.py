from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models, const, const_table, tests2
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from django.http import HttpResponseRedirect

def jrToJson(jr):
    '''将JsonResponse对象转为Json对象'''
    return json.loads(jr.content.decode('utf8'))

class EnterSignupTestCase(TestCase):
    '''测试企业注册Api：enterprise_signup'''
    def setUp(self):
        models.Enterprise.objects.create(
            EID = 'eid1', email = '654321@qq.com', password = 'password1',
            name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1'
        )

    def test_signup(self):
        #测试邮箱已注册
        info = {
            'email': '654321@qq.com',
            'name': 'test_name',
            'password': '12345678'
        }
        rf = RequestFactory()
        request = rf.post('api/enter/signup/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['flag'],
        const_table.const.EMAIL_REGISTERED)
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['flag'],
        const_table.const.SUCCESS)

class EnterLoginTestCase(TestCase):
    '''测试企业登录Api：enterprise_login'''
    def setUp(self):
        md5 = hashlib.md5()
        salt = 'testsalt'
        password = 'password1'
        password += salt
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        models.Enterprise.objects.create(
            EID = 'eid1', email = '654321@qq.com', password = password,
            name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'testsalt'
        )

    def test_login(self):
        #测试登录成功
        info = {
            'email': '654321@qq.com',
            'password': 'password1'
        }
        rf = RequestFactory()
        request = rf.post('api/enter/login/')
        #测试密码错误
        info['password'] = '123456789'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['flag'],
        const_table.const.WRONG_PASSWORD)
        #测试登录失败
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['flag'],
        const_table.const.WRONG_ACCOUNT)

class SendEmailTestCase(TestCase):
    '''发送邮件Api'''
    def test_sendEmail(self):
        #该功能的测试与企业邀请客服的重合
        pass

class ResetCustomerStateTestCase(TestCase):
    '''测试改变客服激活与否的状态Api'''
    def setUp(self):
        models.Customer.objects.create(
            CID = 'test_cid', EID = 'test_eid', email = 'test_email', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
        )

    def test_logoff(self):
        #失败
        info = {'cid': 'cid'}
        rf = RequestFactory()
        request = rf.post('api/enter/reset/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.reset_customer_state(request))['flag'],
        const_table.const.CUSTOMER_NOT_EXIST)
        #成功
        info['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_customer_state(request))
        self.assertEqual(result['message'], 'logoff success')
        models.Customer.objects.filter(CID = 'test_cid').update(state = -1)
        result = jrToJson(enterprise.reset_customer_state(request))
        self.assertEqual(result['message'], 'activate success')

class InviteCustomerTestCase(TestCase):
    '''测试邀请客服Api'''
    def setUp(self):
        models.Customer.objects.create(
            CID = 'test_cid', EID = 'test_eid', email = '123456@qq.com',
            salt = 'testsalt', password = 'test_password', icon = 'test_icon',
            name = 'test_name', state = 1,service_number = 0, serviced_number = 100,
            last_login = datetime.datetime.now()
        )

    def test_invite(self):
        #测试邮箱所属客服已注册过
        info = {
            'eid': 'test_eid',
            'email': '123456@qq.com'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/invite/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_invite(request))['flag'],
        const_table.const.MAILBOX_REGISTERED)

    def test_invite_successful(self):
        info = {
            'eid': 'test_eid1',
            'email': '1234567@qq.com'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/invite/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_invite(request))
        self.assertEqual(result['flag'], const_table.const.SUCCESS)
        self.assertEqual(((result['message']))['email'], '1234567@qq.com')
       
class GetCustomersTestCase(TestCase):
    '''测试获取客服列表Api'''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid1', EID = 'test_eid', email = '1111@qq.com', salt = 'testsalt',
            password = 'test_password1', icon = 'test_icon', name = 'test_name1', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 1,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())
        tests2.DialogsListTestCase.setUp(self)

    def test_get_customers(self):
        rf = RequestFactory()
        info = {}
        request = rf.post('api/enter/get_customers')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'test_eid'
        result = jrToJson(enterprise.enterprise_get_customers(request))['message']
        self.assertEqual(result[0]['cid'], 'test_cid1')
        self.assertEqual(result[1]['cid'], 'test_cid2')
        self.assertEqual(result[0]['avg_feedback'], 4.5)
        self.assertEqual(result[1]['avg_feedback'], 1)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_customers(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class InquireCustomerInfoTestCase(TestCase):
    '''测试根据客服ID查询某个客服信息'''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '1234@qq.com', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
            )

    def test_inquire_info(self):
        #测试客服不存在
        info = {'cid': 'cid'}
        rf = RequestFactory()
        request = rf.post('api/enter/inquireinfo/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.inquire_customer_info(request))['flag'],
        const_table.const.CUSTOMER_NOT_EXIST)
        #测试查询成功
        info['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.inquire_customer_info(request))['message']
        self.assertEqual(result['email'], '1234@qq.com')
        self.assertEqual(result['EID'], 'test_eid')
        self.assertEqual(result['icon'], 'test_icon')
        self.assertEqual(result['name'], 'test_name')
        self.assertEqual(result['state'], 1)
        self.assertEqual(result['service_number'], 0)
        self.assertEqual(result['serviced_number'], 100)

class OnlineCustomersTestCase(TestCase):
    '''测试获取在线客服列表Api'''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid1', EID = 'test_eid1', email = '1111@qq.com', salt = 'testsalt',
            password = 'test_password1', icon = 'test_icon', name = 'test_name1', state = 3,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid1', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 2,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid3', EID = 'test_eid1', email = '3333@qq.com', salt = 'testsalt',
            password = 'test_password3', icon = 'test_icon', name = 'test_name3', state = 2,
            service_number = 0, serviced_number = 109, last_login = datetime.datetime.now())

    def test_online_customers(self):
        rf = RequestFactory()
        info = {}
        request = rf.post('api/enter/test_online_customers/')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'test_eid1'
        result = jrToJson(enterprise.enterprise_online_customers(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['cid'], 'test_cid2')
        self.assertEqual(result[0]['name'], 'test_name2')
        self.assertEqual(result[1]['cid'], 'test_cid3')
        self.assertEqual(result[1]['name'], 'test_name3')
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_online_customers(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class GetTotalTimeTestCase(TestCase):
    '''测试获取企业服务总时间Api'''
    def setUp(self):
        time1 = timezone.now()
        time2 = time1 + datetime.timedelta(minutes = 5)
        time3 = time1 + datetime.timedelta(minutes = 8)
        time4 = time3 + datetime.timedelta(minutes = 3)
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time2)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid2', start_time = time2, end_time = time3)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid1', start_time = time3, end_time = time4)

    def test_total_time(self):
        EID = 'test_eid1'
        result = jrToJson(enterprise.enterprise_total_servicetime(EID))['message']
        self.assertEqual(result, 8.0)

class GetTotalMessagesTestCase(TestCase):
    '''测试获取企业总消息数Api'''
    def setUp(self):
        time1 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Message.objects.create(MID = 'test_mid1', SID = 'test_sid1', RID = 'test_rid1', DID = 'test_did1',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid2', SID = 'test_sid2', RID = 'test_rid2', DID = 'test_did1',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid3', SID = 'test_sid3', RID = 'test_rid3', DID = 'test_did3',
            content = 'test_content', date = time1)
        models.Message.objects.create(MID = 'test_mid4', SID = 'test_sid4', RID = 'test_rid4', DID = 'test_did2',
            content = 'test_content', date = time1)

    def test_total_messages(self):
        EID = 'test_eid1'
        result = jrToJson(enterprise.enterprise_total_messages(EID))['message']
        self.assertEqual(result, 3)

class SetChatboxTypeTestCase(TestCase):
    '''测试更改聊天窗口弹出方式API'''
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', state = 1, salt = 'salt1', chatbox_type = 1)
    
    def test_set_chatbox_type(self):
        rf = RequestFactory()
        info = {
            'chatbox_type': 2
        }
        request = rf.post('api/enter/set_chatbox_type/')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'eid1'
        result = jrToJson(enterprise.enterprise_set_chatbox_type(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_chatbox_type(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)
