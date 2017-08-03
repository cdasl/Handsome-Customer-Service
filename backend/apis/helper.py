#coding:utf-8
from django.core.mail import EmailMultiAlternatives
import time, re
from . import messages

"""encrpypt or decrypt the string"""
 
def encrypt(key, s):   
    """encrypt string(key is a number)"""
    b = bytearray(str(s).encode('utf-8'))
    n = len(b) # 求出 b 的字节数   
    c = bytearray(n*2)   
    j = 0   
    for i in range(0, n):   
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16   
        c2 = b2 // 16 # b2 = c2*16 + c1   
        c1 = c1 + 65   
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码   
        c[j] = c1 
        c[j+1] = c2
        j = j+2   
    return c.decode('utf-8').lower()
 
def decrypt(key, s):
    """decrypt string(key is a number)"""
    c = bytearray(str(s).upper().encode('utf-8'))   
    n = len(c) # 计算 b 的字节数   
    if n % 2 != 0 :   
        return ""   
    n = n // 2   
    b = bytearray(n)   
    j = 0   
    for i in range(0, n):   
        c1 = c[j]   
        c2 = c[j+1]   
        j = j+2   
        c1 = c1 - 65   
        c2 = c2 - 65   
        b2 = c2*16 + c1   
        b1 = b2^ key   
        b[i]= b1   
    try:   
        return b.decode('utf-8')
    except:   
        return ""

def get_active_code(email):
    """get active code by email and current date"""
    key=9
    encry_str='%s|%s' % (email,time.strftime('%Y-%m-%d',time.localtime(time.time())))
    active_code=encrypt(key,encry_str)
    return active_code
 
def send_active_email(email, active_code, mySubject, myMessage):
    """send the active email"""
    subject=mySubject
    message=myMessage
 
    send_to=[email]
    fail_silently=False  #发送异常报错
 
    msg=EmailMultiAlternatives(subject=subject,body=message,to=send_to)
    msg.attach_alternative(message, "text/html")
    msg.send(fail_silently)