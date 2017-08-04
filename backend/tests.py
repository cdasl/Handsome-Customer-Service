from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise
from . import models
import json, hashlib, time, random, string 
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
        #测试注册失败
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['message'], 
            'fail to sign up')

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
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1')
        
    def test_login(self):
        #测试登录成功
        info  =  {    
            'email': '654321@qq.com',
            'password': 'password1'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/login/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['message'], 
            'successful')
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
