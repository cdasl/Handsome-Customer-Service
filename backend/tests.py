from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise
from . import models
import json, datetime
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
            'fail to sign up')

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