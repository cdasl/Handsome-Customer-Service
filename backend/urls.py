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
from . import views, api, socket
from .apis import enterprise, customer

urlpatterns = [
    url(r'^$', api.index, name='index'),
	url(r'^index.html$', TemplateView.as_view(template_name = 'index.html')),
    url(r'^login.html$', TemplateView.as_view(template_name = 'login.html')),
    url(r'^enterprise/$', TemplateView.as_view(template_name = 'enterprise.html')),
    url(r'^enterprise_active/([a-zA-Z]+)$', TemplateView.as_view(template_name = 'enterprise_active.html'), name = 'enterprise_active'),
    url(r'^reset_pwd/$', TemplateView.as_view(template_name = 'reset_password.html')),
    url(r'^enter_manage/$', TemplateView.as_view(template_name = 'enterprise_manage.html')),

    #apis
    url(r'^api/enter/signup/$', enterprise.enterprise_signup, name = 'enter_signup'),
    url(r'^api/enter/login/$', enterprise.enterprise_login, name = 'enter_login'),
    url(r'^api/enter/reset/$', enterprise.reset_customer_state, name = 'reset_customer_state'),
    url(r'^api/active/$', enterprise.enterprise_active, name = 'active'),
    url(r'^user/$', socket.user, name = 'socket'),
    url(r'^socketio*', socket.user, name = 'socketio'),
    url(r'^api/get_customers/$', enterprise.enterprise_get_customers, name = 'get_customers'),
    url(r'^api/reset_password/$', enterprise.reset_password_request, name = 'reset_pwd_request'),
    url(r'^api/new_pwd_submit/$', enterprise.reset_password, name = 'reset_password_submit'),
    url(r'^api/enter/set_robot_message/$', enterprise.enterprise_set_robot_message, name = 'enterprise_set_robot_message'),
    url(r'^api/enter/setuser_message/$', enterprise.enterprise_setuser_message, name = 'enterprise_setuser_message'),
    url(r'^api/enter/customer/login/$', customer.customer_login, name = 'customer_login'),
    url(r'^api/customer/logout/$', customer.customer_logout, name = 'customer_logout'),
    url(r'^api/enter/get_enterprise_msgnum/$', enterprise.enterprise_message_number_oneday),
    url(r'^api/customer/change_ol/$', customer.customer_change_onlinestate),
    url(r'^api/customer/get_serviced_num/$', customer.customer_serviced_number),
    url(r'^api/enter/get_enter_serviced_num/$', enterprise.enterprise_serviced_number_oneday),
    url(r'^api/enter/get_oneday/$', enterprise.enterprise_dialogs_oneday),
    url(r'^api/customer/get_oneday/$', customer.customer_dialogs_oneday),
    url(r'^api/customer/total_msg/$', customer.customer_total_messages),
    url(r'^api/customer/total_minute/$', customer.customer_total_servicedtime),
    url(r'^api/customer/total_dialog/$', customer.customer_total_dialogs),
    url(r'^api/customer/avg_time/$', customer.customer_avgtime_dialogs),
    url(r'^api/customer/avg_msg/$', customer.customer_avgmes_dialogs),
    url(r'^api/enter/get_alldata/$', enterprise.enterprise_get_alldata),
    url(r'^api/customer/dialog_list/$', customer.customer_dialogs),
    url(r'^api/customer/dialog_msg/$', customer.customer_dialog_messages),
    url(r'^api/customer/modify/$', customer.customer_modify_icon),
    url(r'^api/customer/get_alldata/$', customer.customer_get_alldata),
    url(r'^api/customer/get_info/$', customer.customer_get_info),
    url(r'^api/customer/get_id/$', customer.customer_get_id),
    url(r'^api/enter/set_robot_state/$', enterprise.enterprise_set_robot_state),
    url(r'^api/enter/get_robot_info/$', enterprise.enterprise_get_robot_info),
    url(r'^api/enter/set_robot_question/$', enterprise.enterprise_set_robot_question),
    url(r'^api/enter/get_all_question/$', enterprise.enterprise_get_all_question),
    url(r'^api/url_validate/$', enterprise.UrlValidateJudge),
    url(r'^api/enter/chattype/$', enterprise.enterprise_set_chatbox_type),
    url(r'^api/enter/reset_password/$', enterprise.enterprise_changepassword),
    url(r'^api/enter/invite/$', enterprise.enterprise_invite),
    url(r'^api/enter/dialogs/$', enterprise.enterprise_dialogs),
    url(r'^api/enter/dialog_message/$', enterprise.enterprise_dialog_messages),
    url(r'^api/enter/customer_info/$', enterprise.inquire_customer_info),
    url(r'^api/enter/delete_question/$', enterprise.enterprise_delete_question),
    url(r'^api/enter/modify_question/$', enterprise.enterprise_modify_question),
]
