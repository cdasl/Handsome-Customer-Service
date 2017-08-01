from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json, hashlib, time, random, string 
from . import models
from chatterbot import ChatBot


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

def test(request):
    tp = json.loads(request.body.decode('utf8'))
    messages = {
        'message': [
            {'name': '客服', 'content': "你好"},
            {'name': '用户', 'content': "hello"},
            {'name': '客服', 'content': "有什么能帮您"},
            {'name': '用户', 'content': "请问怎么打开手机"},
            {'name': '客服', 'content': "无可奉告"},
            {'name': '用户', 'content': "毕竟too young"},
            {'name': '用户', 'content': "naive"},
            {'name': '客服', 'content': "搞大新闻"},
        ]
    }
    if tp['type'] == 'inner':
        return JsonResponse(messages)

@csrf_exempt
def talk(request):
    return JsonResponse({
        'msg': 'content'
        })
    chatbot = ChatBot(
        'Ron Obvious',
        trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
    )
    mes = json.loads(request.body.decode('utf8'))
    res = chatbot.get_response(mes['mes']).text
    return JsonResponse({
        'res': {
            'content': res
        }
        })