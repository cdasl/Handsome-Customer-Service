from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages
from . import models
import json, hashlib, time, random, string, datetime
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