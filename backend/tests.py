from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
# Create your tests here.

def jrToJson(jr):
    """
        将JsonResponse对象转为Json对象
    """
    return json.loads(jr.content.decode('utf8'))


class EnterSignupTestCase(TestCase):
    """
        测试企业注册Api：enterprise_signup
    """
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1')
        
    def test_signup(self):
        #测试邮箱已注册
        info  =  {    
            'email': '654321@qq.com',
            'name': 'test_name',
            'password': '12345678'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/signup/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['message'],
            'this email has been registered')
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['message'],
            'sign up successfully, please go to check your email')

class EnterLoginTestCase(TestCase):
    """
        测试企业登录Api：enterprise_login
    """
    def setUp(self):
        md5 = hashlib.md5()
        salt = 'testsalt'
        password = 'password1'
        password += salt
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = password,
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'testsalt')
        
    def test_login(self):
        #测试登录成功
        info  =  {    
            'email': '654321@qq.com',
            'password': 'password1'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/login/')
        #测试密码错误
        info['password'] = '123456789'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['message'], 
            'wrong password')
        #测试登录失败
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['message'], 
            'wrong account')

class SendEmailTestCase(TestCase):
    """
        发送邮件Api
    """
    def test_sendEmail(self):
        #该功能的测试与企业邀请客服的重合
        pass

class LogoffCustomerTestCase(TestCase):
    """
        测试注销客服Api
    """
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = 'test_email', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
            )

    def test_logoff(self):
        info = {'cid': 'cid'}
        rf = RequestFactory()
        request = rf.post('api/enter/logoff/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_logoff_customer(request))['message'],
            'not exist this customer')
        info['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_logoff_customer(request))['message'],
            'log off test_name successfully')

class InviteCustomerTestCase(TestCase):
    """
        测试邀请客服Api
    """
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '123456@qq.com', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())

    def test_invite(self):
        #测试邮箱所属客服已注册过
        info = {'email': '123456@qq.com'}
        rf = RequestFactory()
        request = rf.post('api/enter/invite/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_invite(request))['message'],
            'the mailbox has been registered') 
        
class GetCustomersTestCase(TestCase):
    """
        测试获取客服列表Api
    """
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid1', EID = 'test_eid', email = '1111@qq.com', salt = 'testsalt',
            password = 'test_password1', icon = 'test_icon', name = 'test_name1', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 1,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())

    def test_get_customers(self):
        rf = RequestFactory()
        info = {'eid': 'test_eid'}
        request = rf.post('api/enter/test_get_customers')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_get_customers(request))['message']
        self.assertEqual(result[0]['cid'], 'test_cid1')
        self.assertEqual(result[1]['cid'], 'test_cid2')

class InquireCustomerInfoTestCase(TestCase):
    """
        测试根据客服ID查询某个客服信息
    """
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
        self.assertEqual(jrToJson(enterprise.inquire_customer_info(request))['message'], 'not exist this customer')
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
    """
        测试获取在线客服列表Api
    """
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid1', EID = 'test_eid', email = '1111@qq.com', salt = 'testsalt',
            password = 'test_password1', icon = 'test_icon', name = 'test_name1', state = 3,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 2,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid3', EID = 'test_eid', email = '3333@qq.com', salt = 'testsalt',
            password = 'test_password3', icon = 'test_icon', name = 'test_name3', state = 2,
            service_number = 0, serviced_number = 109, last_login = datetime.datetime.now())

    def test_online_customers(self):
        rf = RequestFactory()
        info = {'eid': 'test_eid'}
        request = rf.post('api/enter/test_online_customers/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_online_customers(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['cid'], 'test_cid2')
        self.assertEqual(result[0]['name'], 'test_name2')
        self.assertEqual(result[1]['cid'], 'test_cid3')
        self.assertEqual(result[1]['name'], 'test_name3')

class GetTotalTimeTestCase(TestCase):
    """
        测试获取企业服务总时间Api
    """
    def setUp(self):
        time1 = timezone.now()
        time2 = time1 + datetime.timedelta(minutes = 5)
        time3 = time1 + datetime.timedelta(minutes = 8)
        time4 = time3 + datetime.timedelta(minutes = 3)
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time2)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid2', start_time = time2, end_time = time3)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid1', start_time = time3, end_time = time4)

    def test_total_time(self):
        rf = RequestFactory()
        info = {'eid': 'test_eid1'}
        request = rf.post('api/enter/total_time/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_total_servicetime(request))['message']
        self.assertEqual(result, 8.0)

class GetTotalMessagesTestCase(TestCase):
    """
        测试获取企业总消息数Api
    """
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
        rf = RequestFactory()
        info = {'eid': 'test_eid1'}
        request = rf.post('api/enter/total_time/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_total_messages(request))['message']
        self.assertEqual(result, 3)

class GetCountOfDialogsTestCase(TestCase):
    """
        测试获取企业总会话数Api
    """
    def setUp(self):
        time1 = timezone.now()
        models.Dialog.objects.create(DID = 'test_did1', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did2', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did3', EID = 'test_eid1', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did4', EID = 'test_eid3', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did5', EID = 'test_eid2', start_time = time1, end_time = time1)
        models.Dialog.objects.create(DID = 'test_did6', EID = 'test_eid1', start_time = time1, end_time = time1)

    def test_count_of_dialogs(self):
        rf = RequestFactory()
        info = {'eid': 'test_eid1'}
        request = rf.post('api/enter/total_dialogs/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_total_dialogs(request))['message']
        self.assertEqual(result, 3)

class GetChattedTestCase(TestCase):
    """
        测试获取与某位客服聊过天的所有用户Api
    """
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
    """
        测试获取企业全部会话列表Api
    """
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
        info = {'eid': 'test_eid1'}
        request = rf.post('api/enter/test_dialogs_list/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_dialogs(request))['message']
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['did'], 'test_did1')
        self.assertEqual(result[1]['did'], 'test_did2')

class ResetPasswordTestCase(TestCase):
    '''
        测试重置密码API
    '''
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
        result = jrToJson(enterprise.reset_password_request(request))['message']
        self.assertEqual(result, 'invalid')
    
    def test_reset_partone(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #企业
        info = {'active_code': 'pdmdndkdldidjeihihhckgggegfhldjdidodecjdbdecjdmd', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['message']
        self.assertEqual(result, 'reset')
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
        result = jrToJson(enterprise.reset_password(request))['message']
        self.assertEqual(result, 'invalid')

    def test_reset_parttwo(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #客服
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdmd', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['message']
        self.assertEqual(result, 'reset')
        #激活码过期
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdid', 
                'password': '7dsa987d9a8s'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['message']
        self.assertEqual(result, 'expired')

class DialogMessagesTestCase(TestCase):
    """
        测试获取会话内容Api
    """
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