from django.contrib import admin
from .models import Enterprise, Customer, User, Dialog, Message, Question 
# Register your models here.

admin.site.register(Enterprise)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Dialog)
admin.site.register(Message)
admin.site.register(Question)