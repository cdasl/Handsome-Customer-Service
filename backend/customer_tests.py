from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from . import tests

class CustomerLoginTestCase(TestCase):
    """
        测试用户登录Api
    """
    def setUp(self):
        md5 = hashlib.md5()
        salt = 'testsalt'
        password = 'password1'
        password += salt
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '2222@qq.com', salt = salt,
            password = password, icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
        )

    def test_login(self):
        #测试登录成功
        info = {    
            'email': '2222@qq.com',
            'password': 'password1'
        }
        rf = RequestFactory()
        request = rf.post('api/enter/customer/login/')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        self.assertEqual(tests.jrToJson(customer.customer_login(request))['flag'], 1)
        #测试密码错误
        info['password'] = '123456789'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_login(request))['flag'], -1)
        #测试登录失败
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_login(request))['flag'], -7)

class CustomerLogoutTestCase(TestCase):
    '''
        测试客服退出Api
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '2222@qq.com', salt = 'salt',
            password = 'password', icon = 'test_icon', name = 'test_name', state = 2,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
        )

    def test_logout(self):
        rf = RequestFactory()
        request = rf.post('api/customer/logout/')
        request.session = {}
        #登出失败
        info = {}
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_logout(request))['flag'], -12)
        #登出成功
        request.session['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_logout(request))['flag'], 1)

class OnlineStateTestCase(TestCase):
    '''
    测试改变在线状态
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '2222@qq.com', salt = 'salt',
            password = 'password', icon = 'test_icon', name = 'test_name', state = 2,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
        )

    def test_online_state_change(self):
        rf = RequestFactory()
        request = rf.post('api/customer/change_ol/')
        request.session =  {}
        info = {}
        #失败
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_change_onlinestate(request))['flag'], -12)
        #成功
        request.session['cid'] = 'test_cid'
        self.assertEqual(tests.jrToJson(customer.customer_change_onlinestate(request))['flag'], 1)
        self.assertEqual(models.Customer.objects.get(CID = 'test_cid').state, 3)
        self.assertEqual(tests.jrToJson(customer.customer_change_onlinestate(request))['flag'], 1)
        self.assertEqual(models.Customer.objects.get(CID = 'test_cid').state, 2)

class ServicedNumTestCase(TestCase):
    '''
        测试客服服务过的人数
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '2222@qq.com', salt = 'salt',
            password = 'password', icon = 'test_icon', name = 'test_name', state = 2,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
        )

    def test_serviced_number(self):
        rf = RequestFactory()
        request = rf.post('api/customer/get_serviced_num/')
        request.session =  {}
        info = {}
        #成功
        request.session['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_serviced_number(request))['message'], 100)









