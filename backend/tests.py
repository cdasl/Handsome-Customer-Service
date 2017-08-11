from django.test import TestCase
from django.test.client import RequestFactory
from .apis import enterprise, helper, messages, customer
from . import models
import json, hashlib, time, random, string, datetime
import django.utils.timezone as timezone
# Create your tests here.

def jrToJson(jr):
    '''
        将JsonResponse对象转为Json对象
    '''
    return json.loads(jr.content.decode('utf8'))


class EnterSignupTestCase(TestCase):
    '''
        测试企业注册Api：enterprise_signup
    '''
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
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['flag'], -3)
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_signup(request))['flag'], 1)

class EnterLoginTestCase(TestCase):
    '''
        测试企业登录Api：enterprise_login
    '''
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
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['flag'], -1)
        #测试登录失败
        info['email'] = '123456@qq.com'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_login(request))['flag'], -7)

class SendEmailTestCase(TestCase):
    '''
        发送邮件Api
    '''
    def test_sendEmail(self):
        #该功能的测试与企业邀请客服的重合
        pass

class ResetCustomerStateTestCase(TestCase):
    '''
        测试改变客服激活与否的状态Api
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = 'test_email', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now()
            )

    def test_logoff(self):
        #失败
        info = {'cid': 'cid'}
        rf = RequestFactory()
        request = rf.post('api/enter/reset/')
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.reset_customer_state(request))['flag'], -13)
        #成功
        info['cid'] = 'test_cid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.reset_customer_state(request))['message'], 'logoff success')
        models.Customer.objects.filter(CID = 'test_cid').update(state = -1)
        self.assertEqual(jrToJson(enterprise.reset_customer_state(request))['message'], 'activate success')

class InviteCustomerTestCase(TestCase):
    '''
        测试邀请客服Api
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid', EID = 'test_eid', email = '123456@qq.com', salt = 'testsalt',
            password = 'test_password', icon = 'test_icon', name = 'test_name', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())

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
            -10)

    def test_invite_successful(self):
        info = {
            'eid': 'test_eid1',
            'email': '1234567@qq.com'
            }
        rf = RequestFactory()
        request = rf.post('api/enter/invite/')
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.enterprise_invite(request))
        self.assertEqual(result['flag'], 1)
        self.assertEqual(((result['message']))['email'], '1234567@qq.com')
       
class GetCustomersTestCase(TestCase):
    '''
        测试获取客服列表Api
    '''
    def setUp(self):
        models.Customer.objects.create(CID = 'test_cid1', EID = 'test_eid', email = '1111@qq.com', salt = 'testsalt',
            password = 'test_password1', icon = 'test_icon', name = 'test_name1', state = 1,
            service_number = 0, serviced_number = 100, last_login = datetime.datetime.now())
        models.Customer.objects.create(CID = 'test_cid2', EID = 'test_eid', email = '2222@qq.com', salt = 'testsalt',
            password = 'test_password2', icon = 'test_icon', name = 'test_name2', state = 1,
            service_number = 0, serviced_number = 10, last_login = datetime.datetime.now())

    def test_get_customers(self):
        rf = RequestFactory()
        info = {}
        request = rf.post('api/enter/test_get_customers')
        request._body = json.dumps(info).encode('utf8')
        request.session = {}
        request.session['eid'] = 'test_eid'
        result = jrToJson(enterprise.enterprise_get_customers(request))['message']
        self.assertEqual(result[0]['cid'], 'test_cid1')
        self.assertEqual(result[1]['cid'], 'test_cid2')
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_customers(request))['flag']
        self.assertEqual(result, -12)

class InquireCustomerInfoTestCase(TestCase):
    '''
        测试根据客服ID查询某个客服信息
    '''
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
        self.assertEqual(jrToJson(enterprise.inquire_customer_info(request))['flag'], -13)
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
    '''
        测试获取在线客服列表Api
    '''
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
        self.assertEqual(result, -12)

class GetTotalTimeTestCase(TestCase):
    '''
        测试获取企业服务总时间Api
    '''
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
    '''
        测试获取企业总消息数Api
    '''
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

class GetCountOfDialogsTestCase(TestCase):
    '''
        测试获取企业总会话数Api
    '''
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
    '''
        测试获取与某位客服聊过天的所有用户Api
    '''
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
    '''
        测试获取企业全部会话列表Api
    '''
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
        self.assertEqual(result, -12)

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
        result = jrToJson(enterprise.reset_password_request(request))['flag']
        self.assertEqual(result, -8)
    
    def test_reset_partone(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #企业 时间问题，间隔时间太长会显示过期
        info = {'active_code': 'pdmdndkdldidjeihihhckgggegfhldjdidadecjdbdecjdid', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, 1)
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
        self.assertEqual(result, -8)

    def test_reset_parttwo(self):
        rf = RequestFactory()
        request = rf.post('api/new_pwd_submit/')
        #客服 时间有问题，时间太长会显示过期
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdmd', 
                'password': '11111111'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, -9)
        #激活码过期
        info = {'active_code': 'ldldldldjeihihhckgggegfhldjdidodecjdbdecjdid', 
                'password': '7dsa987d9a8s'}
        request._body = json.dumps(info).encode('utf8')
        result = jrToJson(enterprise.reset_password(request))['flag']
        self.assertEqual(result, -9)

class DialogMessagesTestCase(TestCase):
    '''
        测试获取会话内容Api
    '''
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
    '''
        测试改企业机器人名字API
    '''
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
        self.assertEqual(result, 1)
        test_case1 = models.Enterprise.objects.get(EID = 'eid1').robot_name
        self.assertEqual('test1', test_case1)
        test_case2 = models.Enterprise.objects.get(EID = 'eid1').robot_icon
        self.assertEqual('test2', test_case2)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_message(request))['flag']
        self.assertEqual(result, -12)

class MessagesBetweenChattersTestCase(TestCase):
    '''
        测试根据聊天者ID获取聊天内容Api
    '''
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
    '''
        测试获取企业会话平均消息数Api
    '''
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
    '''
        测试获取企业会话平均时间Api
    '''
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

class SetChatboxTypeTestCase(TestCase):
    '''
        测试更改聊天窗口弹出方式API
    '''
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
        self.assertEqual(result, 1)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_chatbox_type(request))['flag']
        self.assertEqual(result, -12)

class SetUserMsgTestCase(TestCase):
    '''
        测试设置企业发送用户信息
    '''
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
        self.assertEqual(result, 1)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_setuser_message(request))['flag']
        self.assertEqual(result, -12)

class EnterpriseMsgNumTestCase(TestCase):
    '''
        测试企业24h内的消息数
    '''
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
        self.assertEqual(result, 1)
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_message_number_oneday(request))['flag']
        self.assertEqual(result, -12)

class EnterServicedNumTestCase(TestCase):
    '''
        测试企业24h服务的人数
    '''
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
        self.assertEqual(result, 1)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_serviced_number_oneday(request))['flag']
        self.assertEqual(result, -12)

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
        self.assertEqual(result, 1)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_dialogs_oneday(request))['flag']
        self.assertEqual(result, -12)

class AllDataTestCase(TestCase):
    '''测试返回企业所有信息'''
    def setUp(self):
        EnterServicedNumTestCase.setUp(self)
        OnlineCustomersTestCase.setUp(self)
    def test_all_data(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_alldata/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'test_eid1' 
        result = jrToJson(enterprise.enterprise_get_alldata(request))['flag']
        self.assertEqual(result, 1)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_alldata(request))['flag']
        self.assertEqual(result, -12)

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
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'], 1)
        self.assertEqual(models.Enterprise.objects.get(EID = 'eid1').state, 1)
        #已激活
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'], -12)
        #过期
        info['active_code'] = 'pdmdndkdldidjeihihhckgggegfhldjdidjdecjdbdecjdid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'], -9)
        #无效
        info['active_code'] = 'pdmdcidsjicohdsiohcoidshciodhscoidjdecjdbdecjdid'
        request._body = json.dumps(info).encode('utf8')
        self.assertEqual(jrToJson(enterprise.enterprise_active(request))['flag'], -8)

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

class EnterpriseRobotStateTestCase(TestCase):
    '''测试企业设置机器人状态'''
    def setUp(self):
        EnterSignupTestCase.setUp(self)

    def test_set_robot_state(self):
        rf = RequestFactory()
        request = rf.post('api/enter/set_robot_state/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'eid1' 
        result = jrToJson(enterprise.enterprise_set_robot_state(request))['flag']
        self.assertEqual(result, 1)
        self.assertEqual(models.Enterprise.objects.get(EID = 'eid1').robot_state, 1)
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_state(request))['flag']
        self.assertEqual(result, -12)

class GetRobotInfoTestCase(TestCase):
    '''测试企业获取机器人信息'''
    def setUp(self):
        SetRobotMessageTestCase.setUp(self)

    def test_get_robot_info(self):
        rf = RequestFactory()
        request = rf.post('api/enter/get_robot_info/')
        info = {}
        request.session = {}
        request._body = json.dumps(info).encode('utf8')
        #成功
        request.session['eid'] = 'eid1' 
        result = jrToJson(enterprise.enterprise_get_robot_info(request))
        self.assertEqual(result['flag'], 1)
        self.assertEqual((result['message'])['robot_name'], 'rn1')
        self.assertEqual((result['message'])['robot_icon'], 'ri1')
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_robot_info(request))['flag']
        self.assertEqual(result, -12)

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
        self.assertEqual(result['flag'], 1)
        test = models.Question.objects.get(category = 'Life')
        self.assertEqual(test.question, 'Why should you die?')
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_set_robot_question(request))['flag']
        self.assertEqual(result, -12)

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
        #失败
        del request.session['eid']
        result = jrToJson(enterprise.enterprise_get_all_question(request))['flag']
        self.assertEqual(result, -12)
