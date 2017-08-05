'''handsome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
'''
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls import include
from . import views, api,socket
from .apis import enterprise

urlpatterns = [
    url(r'^$', api.index, name='index'),
	url(r'^index.html$', TemplateView.as_view(template_name = 'index.html')),
    url(r'^login.html$', TemplateView.as_view(template_name = 'login.html')),
    url(r'^enterprise/$', TemplateView.as_view(template_name = 'enterprise.html')),
    url(r'^enterprise_active/([a-zA-Z]+)$', TemplateView.as_view(template_name = 'enterprise_active.html'), name = 'enterprise_active'),
    url(r'^reset_pwd/$', TemplateView.as_view(template_name = 'reset_password.html')),

    #apis
    url(r'^api/enter/signup/$', enterprise.enterprise_signup, name = 'enter_signup'),
    url(r'^api/enter/login/$', enterprise.enterprise_login, name = 'enter_login'),
    url(r'^api/enter/logoff/$', enterprise.enterprise_logoff_customer, name = 'enter_logoff'),
    url(r'^api/active/$', enterprise.enterprise_active, name = 'active'),
    url(r'^user/$', socket.user, name = 'socket'),
    url(r'^socketio*', socket.user, name = 'socketio'),
    url(r'^api/get_customers/$', enterprise.enterprise_get_customers, name = 'get_customers'),
    url(r'^api/reset_password/$', enterprise.reset_password_request, name = 'reset_pwd_request'),
    url(r'^api/new_pwd_submit/$', enterprise.reset_password, name = 'reset_password_submit'),
    url(r'^api/enter/set_robot_name/$', enterprise.enterprise_set_robot_name, name = 'enterprise_set_robot_name'),
]