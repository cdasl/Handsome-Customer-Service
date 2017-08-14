from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models, const, const_table, tests, tests2
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
from django.http import HttpResponseRedirect

def jrToJson(jr):
    '''将JsonResponse对象转为Json对象'''
    return json.loads(jr.content.decode('utf8'))

class EnterpriseRobotStateTestCase(TestCase):
    '''测试企业设置机器人状态'''
    def setUp(self):
        tests.EnterSignupTestCase.setUp(self)

    def test_set_robot_state(self):
        rf = RequestFactory()
        request = rf.post('api/enter/set_robot_state/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'eid1' 
        result = jrToJson(enterprise.enterprise_set_robot_state(request))['flag']
        self.assertEqual(result, const_table.const.SUCCESS)
        self.assertEqual(models.Enterprise.objects.get(EID = 'eid1').robot_state, 1)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_state(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class GetRobotInfoTestCase(TestCase):
    '''测试企业获取机器人信息'''
    def setUp(self):
        tests2.SetRobotMessageTestCase.setUp(self)

    def test_get_robot_info(self):
        rf = RequestFactory()
        request = rf.post('api/enter/robot_into/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'eid1' 
        result = jrToJson(enterprise.enterprise_get_robot_info(request))
        self.assertEqual(result['flag'], const_table.const.SUCCESS)
        self.assertEqual((result['message'])['robot_name'], 'rn1')
        self.assertEqual((result['message'])['robot_icon'], 'ri1')
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_robot_info(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class SetRobotQuestionTestCase(TestCase):
    '''测试设置机器人'''
    def test_set_robot_question(self):
        rf = RequestFactory()
        request = rf.post('api/enter/set_robot_question/')
        info = {
            'question': 'Why should you die?',
            'answer': "I don't know.",
            'category': 'Life'
        }
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'eid1' 
        result = jrToJson(enterprise.enterprise_set_robot_question(request))
        self.assertEqual(result['flag'], const_table.const.SUCCESS)
        test = models.Question.objects.get(category = 'Life')
        self.assertEqual(test.question, 'Why should you die?')
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_question(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class EnterpriseGetAllQuestionTestCase(TestCase):
    '''测试返回企业所有问题'''
    def setUp(self):
        models.Question.objects.create(QID = 1, EID = 'test_eid1', question = 'f', 
            answer = 'u', category = 'n')
        models.Question.objects.create(QID = 2, EID = 'test_eid1', question = 'k', 
            answer = 'k', category = 'k')
        models.Question.objects.create(QID = 3, EID = 'test_eid1', question = 'l', 
            answer = 'a', category = 'o')
        models.Question.objects.create(QID = 4, EID = 'test_eid2', question = 't', 
            answer = 't', category = 't')
    def test_get_all_question(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_all_question/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1'
        response = enterprise.enterprise_get_all_question(request)
        result = jrToJson(enterprise.enterprise_get_all_question(request))['message']
        self.assertEqual((result[1])['question'], 'k')
        self.assertEqual(response.status_code, 200)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_all_question(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class UrlValidateTestCase(TestCase):
    '''测试访问是否含有session'''
    def setUp(self):
        tests.EnterSignupTestCase.setUp(self)

    def test_url_valid(self):
        rf = RequestFactory()
        request = rf.post('api/url_validate/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #没有eid
        result = jrToJson(enterprise.UrlValidateJudge(request))
        self.assertEqual(result['flag'], const_table.const.EID_NOT_EXIST)
        #eid错误
        request.session['eid'] = 'hahaha'
        result = jrToJson(enterprise.UrlValidateJudge(request))
        self.assertEqual(result['flag'], const_table.const.ERROR)

class DeleteQuestionTestCase(TestCase):
    '''测试企业删除问题'''
    def setUp(self):
        EnterpriseGetAllQuestionTestCase.setUp(self)

    def test_delete_question(self):
        rf = RequestFactory()
        request = rf.post('api/enter/delete_question/')
        info = {
            'qid': '2'
        }
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1'
        response = enterprise.enterprise_delete_question(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(models.Question.objects.filter(QID = '2')), 0)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_delete_question(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)

class EnterpriseModifyQuestionTestCase(TestCase):
    '''测试企业修改问题'''
    def setUp(self):
        EnterpriseGetAllQuestionTestCase.setUp(self)

    def test_modify_question(self):
        rf = RequestFactory()
        request = rf.post('api/enter/modify_question/')
        info = {
            'qid': '2', 
            'question': '777', 
            'answer': 'TTT', 
            'category': 'fun'
        }
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1'
        response = enterprise.enterprise_modify_question(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual((models.Question.objects.get(QID = '2')).answer, 'TTT')
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_modify_question(request))['flag']
        self.assertEqual(result, const_table.const.EID_NOT_EXIST)
