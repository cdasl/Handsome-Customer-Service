from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models, const, const_table, tests
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from django.http import HttpResponseRedirect

def jrToJson(jr):
    '''将JsonResponse对象转为Json对象'''
    return json.loads(jr.content.decode('utf8'))

class SetUserMsgTestCase(TestCase):
    '''测试设置企业发送用户信息'''
    def test_setuser_message(self):
        rf = RequestFactory()
        info = {
            'uid': 'sssss'
        }
        request = rf.post('api/enter/setuser_message')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'eid1'
        result = jrToJson(enterprise.enterprise_setuser_message(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_setuser_message(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class EnterpriseMsgNumTestCase(TestCase):
    '''测试企业24h内的消息数'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', EID = 'test_eid1', 
                                    start_time = '2017-8-10 17:00:00',
                                    end_time = '2017-8-10 18:00:00')
        models.Dialog.objects.create(DID = '2', EID = 'test_eid1', 
                                    start_time = '2017-8-10 17:00:00',
                                    end_time = '2017-8-10 18:00:00')
        models.Dialog.objects.create(DID = '3', EID = 'test_eid1', 
                                    start_time = '2017-8-1 17:00:00',
                                    end_time = '2017-8-1 18:00:00')
        models.Dialog.objects.create(DID = '4', EID = 'test_eid2', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Message.objects.create(MID = 'a', SID = 'wang', RID = 'zhang', DID = '1',
                                    content = '123', date = '2017-8-29 17:00:00')
        models.Message.objects.create(MID = 'b', SID = 'wang', RID = 'zhang', DID = '1',
                                    content = '123', date = '2017-8-29 17:15:00')
        models.Message.objects.create(MID = 'c', SID = 'wang', RID = 'zhang', DID = '2',
                                    content = '123', date = '2017-8-29 10:00:00')
        models.Message.objects.create(MID = 'd', SID = 'wang', RID = 'zhang', DID = '2',
                                    content = '123', date = '2017-8-10 12:08:00')
        models.Message.objects.create(MID = 'e', SID = 'wang', RID = 'zhang', DID = '3',
                                    content = '123', date = '2017-8-1 17:00:00')
        models.Message.objects.create(MID = 'f', SID = 'wang', RID = 'zhang', DID = '3',
                                    content = '123', date = '2017-8-1 17:00:00')
        models.Message.objects.create(MID = 'g', SID = 'wang', RID = 'zhang', DID = '4',
                                    content = '123', date = '2017-8-9 17:00:00')
        
    def test_enterprise_msg_number(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_enterprise_msgnum')
        info = {}
        request.session = {}
        request.session['eid'] = 'test_eid1' 
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_message_number_oneday(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_message_number_oneday(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class EnterServicedNumTestCase(TestCase):
    '''测试企业24h服务的人数'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', EID = 'test_eid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-29 18:00:00', UID = 7)
        models.Dialog.objects.create(DID = '2', EID = 'test_eid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-29 18:00:00', UID = 77)
        models.Dialog.objects.create(DID = '3', EID = 'test_eid1', 
                                    start_time = '2017-8-1 17:00:00',
                                    end_time = '2017-8-9 18:00:00', UID = 7)
        models.Dialog.objects.create(DID = '4', EID = 'test_eid2', 
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

    def test_enter_serviced_num(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_enter_serviced_num/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1' 
        result = jrToJson(enterprise.enterprise_serviced_number_oneday(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_serviced_number_oneday(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class DialoginOneDayTestCase(TestCase):
    '''测试一天内的对话量'''
    def setUp(self):
        models.Dialog.objects.create(DID = '1', EID = 'test_eid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '2', EID = 'test_eid1', 
                                    start_time = '2017-8-29 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '3', EID = 'test_eid1', 
                                    start_time = '2017-8-1 17:00:00',
                                    end_time = '2017-8-9 18:00:00')
        models.Dialog.objects.create(DID = '4', EID = 'test_eid2', 
                                    start_time = '2017-8-9 17:00:00',
                                    end_time = '2017-8-9 18:00:00')

    def test_oneday(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_oneday/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1' 
        result = jrToJson(enterprise.enterprise_dialogs_oneday(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_dialogs_oneday(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class AllDataTestCase(TestCase):
    '''测试返回企业所有信息'''
    def setUp(self):
        EnterServicedNumTestCase.setUp(self)
        tests.OnlineCustomersTestCase.setUp(self)
    def test_all_data(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_alldata/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1' 
        result = jrToJson(enterprise.enterprise_get_alldata(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_alldata(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class EnterpriseActiveTestCase(TestCase):
    '''测试企业激活'''
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = '654321@qq.com', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1', state = 0)
    
    def test_active(self):
        info = {
            'active_code': 'pdmdndkdldidjeihihhckgggegfhldjdidadecjdbdecjdid'
        }
        rf = RequestFactory()
        request = rf.post('api/active/')
        request._body = json.dumps(info).encode('utf8')
        #成功
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'],
        const_table.const.SUCCESS)
        self.assertEqual(models.Enterprise.objects.get(EID = 'eid1').state, 1)
        #已激活
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'],
        const_table.const.EID_NOT_EXIST)
        #过期
        info['active_code'] = 'pdmdndkdldidjeihihhckgggegfhldjdidjdecjdbdecjdid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'],
        const_table.const.EXPIRED)
        #无效
        info['active_code'] = 'pdmdcidsjicohdsiohcoidshciodhscoidjdecjdbdecjdid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'],
        const_table.const.INVALID)

class EnterpriseTotalServicedNumTestCase(TestCase):
    '''测试企业服务总人数'''
    def setUp(self):
        EnterServicedNumTestCase.setUp(self)

    def test_total_serviced_num(self):
        EID = 'test_eid1'
        result =  jrToJson(enterprise.enterprise_total_service_number(EID))['message']
        self.assertEqual(result, 2)

class EnterpriseDialogtotalOnedayTestCase(TestCase):
    '''测试企业24h会话数'''
    def setUp(self):
        EnterServicedNumTestCase.setUp(self)

    def test_dialog_total_oneday(self):
        EID = 'test_eid1'
        result =  jrToJson(enterprise.enterprise_dialogs_total_oneday(EID))['message']
        self.assertEqual(result, 2)
