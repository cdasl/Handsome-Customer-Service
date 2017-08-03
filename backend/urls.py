"""handsome URL Configuration

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
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls import include
from . import views, api,socket
from .apis import enterprise

urlpatterns = [
    url(r'^$', api.index, name="index"),
	url(r'^index.html$', TemplateView.as_view(template_name="index.html")),
    url(r'^login.html$', TemplateView.as_view(template_name="login.html")),
    url(r'^enterprise/$', TemplateView.as_view(template_name="Enterprise.html")),
    url(r'^user',socket.user),
    url(r'^socketio*',socket.user),
    #apis
    url(r'^api/test/$', api.test, name="test"),
    url(r'^api/enter/signup/$', enterprise.enterprise_signup, name="enter_signup"),
    url(r'^api/enter/login/$', enterprise.enterprise_login, name="enter_login"),
    url(r'^api/talk/$', api.talk, name="talk"),
]

