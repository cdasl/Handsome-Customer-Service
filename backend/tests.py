from django.test import TestCase
from .apis import enterprise
from . import models
import json
# Create your tests here.

def jrToJson(jr):
    """
        将JsonResponse对象转为Json对象
    """
    return json.loads(jr.content.decode('utf8'))


class EnterSignupTestCase(TestCase):
    """
        测试企业注册Api
    """
    def setUp(self):
        models.Enterprise.objects.create(EID = 'eid1', email = 'email1', password = 'password1',
             name = 'name1', robot_icon = 'ri1', robot_name = 'rn1', salt = 'salt1')
        
    def test_signup(self):
        info  =  {    
            'email': 'test_email',
            'name': 'test_name',
            'password': '123456'
            }
        self.assertEqual(jrToJson(enterprise.enterprise_signup_helper(info))['message'], 'sign up successfully, please go to check your email')
        info['email']  =  'email1'
        self.assertEqual(jrToJson(enterprise.enterprise_signup_helper(info))['message'], 'this email has been registered')
        