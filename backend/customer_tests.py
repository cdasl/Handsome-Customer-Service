from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from . import tests

class CustomerLoginTestCase(TestCase):
    """测试用户登录Api"""
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
    """测试客服退出Api"""
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
    """测试改变在线状态"""
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
    """测试客服服务过的人数"""
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
        #失败
        del request.session['cid']
        self.assertEqual(tests.jrToJson(customer.customer_serviced_number(request))['flag'], -12)     

class CustomerOnedayTestCase(TestCase):
    '''测试客服24h的会话数'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', CID = 'test_cid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '2', CID = 'test_cid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '3', CID = 'test_cid1', 
                                    start_time = '2017-8-1 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '4', CID = 'test_cid2', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
    
    def test_customer_oneday(self):
        rf = RequestFactory()
        request = rf.post('api/customer/get_oneday/')
        request.session =  {}
        info = {}
        #成功
        request.session['cid'] = 'test_cid1'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_dialogs_oneday(request))['message'], 2)
        #失败
        del request.session['cid']
        self.assertEqual(tests.jrToJson(customer.customer_dialogs_oneday(request))['flag'], -12)

class CustomerTotalMsgTestCase(TestCase):
    '''测试客服总消息数'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', CID = 'test_cid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '2', CID = 'test_cid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '3', CID = 'test_cid1', 
                                    start_time = '2017-8-1 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '4', CID = 'test_cid2', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Message.objects.create(MID = 'a', SID = 'wang', RID = 'zhang', DID = '1',
                                    content = '123', date = '2017-8-29 17:00:00')
        models.Message.objects.create(MID = 'b', SID = 'wang', RID = 'lee', DID = '1',
                                    content = '123', date = '2017-8-29 17:00:00')
        models.Message.objects.create(MID = 'c', SID = 'wang', RID = 'zhao', DID = '2',
                                    content = '123', date = '2017-8-29 17:00:00')
        models.Message.objects.create(MID = 'd', SID = 'wang', RID = 'zhang', DID = '2',
                                    content = '123', date = '2017-8-29 17:00:00')
        models.Message.objects.create(MID = 'e', SID = 'wang', RID = 'zhang', DID = '3',
                                    content = '123', date = '2017-8-1 17:00:00')
        models.Message.objects.create(MID = 'f', SID = 'wang', RID = 'zhang', DID = '3',
                                    content = '123', date = '2017-8-1 17:00:00')
        models.Message.objects.create(MID = 'g', SID = 'wang', RID = 'zhang', DID = '4',
                                    content = '123', date = '2017-8-9 17:00:00')

    def test_customer_total_msg(self):
        rf = RequestFactory()
        request = rf.post('api/customer/total_msg/')
        request.session =  {}
        info = {}
        #成功
        request.session['cid'] = 'test_cid1'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(tests.jrToJson(customer.customer_total_messages(request))['message'], 6)
        #失败
        del request.session['cid']
        self.assertEqual(tests.jrToJson(customer.customer_total_messages(request))['flag'], -12)

class CustomerTotalServicedTimeTestCase(TestCase):
    '''测试客服服务的总分钟'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', CID = 'test_cid1', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '2', CID = 'test_cid1', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 17:30:05')
        models.Dialog.objects.create(DID = '3', CID = 'test_cid1', 
                                    start_time = '2017-8-9 17:05:32',
                                    end_time = '2017-8-9 17:27:01')
        models.Dialog.objects.create(DID = '4', CID = 'test_cid2', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')

    def test_customer_total_minute(self):
        rf = RequestFactory()
        request = rf.post('api/customer/total_minute/')
        request.session =  {}
        info = {}
        #成功
        request.session['cid'] = 'test_cid1'
        request._body = json.dumps(info).encode('utf8')
        self.assertAlmostEqual(tests.jrToJson(customer.customer_total_servicedtime(request))['message'], 112, delta = 1)
        #失败
        del request.session['cid']
        self.assertEqual(tests.jrToJson(customer.customer_total_servicedtime(request))['flag'], -12)
    



       










