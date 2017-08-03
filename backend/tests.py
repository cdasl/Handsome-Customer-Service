from django.test import TestCase
from .apis import enterprise
from . import models
import json
# Create your tests here.

def jrToJson(jr):
    """
        convert a JsonResponse object into a json object
    """
    return json.loads(jr.content.decode('utf8'))


class EnterSignupTestCase(TestCase):
    """
        test api of signing up for enterprise
    """
    def setUp(self):
        models.Enterprise.objects.create(EID='eid1', email='email1', password='password1',
             name='name1', robot_icon='ri1', robot_name='rn1', salt='salt1')
    def test_signup(self):
        info = {    
            'email': 'test_email',
            'name': 'test_name',
            'password': '123456'
            }
        self.assertEqual(jrToJson(enterprise.enterprise_signup_helper(info))['message'], '注册成功')
        info['email'] = 'email1'
        self.assertEqual(jrToJson(enterprise.enterprise_signup_helper(info))['message'], '该邮箱已注册')
        