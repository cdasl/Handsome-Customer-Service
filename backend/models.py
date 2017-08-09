from django.db import models

# Create your models here.

#enterprise
class Enterprise(models.Model):
    EID = models.CharField(max_length = 50, primary_key = True)
    email = models.CharField(max_length = 30)
    password = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    robot_icon = models.CharField(max_length = 50)
    robot_name = models.CharField(max_length = 10)
    state = models.IntegerField(default = 0)
    salt = models.CharField(max_length = 8)
    chatbox_type = models.IntegerField(default = 1)
    robot_state = models.IntegerField(default = 0)
    def __str__(self):
        return self.email + ',' + self.name

#customer
class Customer(models.Model):
    CID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    email = models.CharField(max_length = 30)
    password = models.CharField(max_length = 50)
    icon = models.CharField(max_length = 50)
    name = models.CharField(max_length = 10)
    state = models.IntegerField(default = 0)
    service_number = models.IntegerField(default = 0)
    serviced_number = models.IntegerField(default = 0)
    last_login = models.DateField()
    salt = models.CharField(max_length = 8)
    def __str__(self):
        return self.email + ',' + self.name

#user
class User(models.Model):
    UID = models.CharField(max_length = 50, primary_key = True)

#dialog
class Dialog(models.Model):
    DID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

#messages
class Message(models.Model):
    MID = models.CharField(max_length = 50, primary_key = True)
    SID = models.CharField(max_length = 50)
    RID = models.CharField(max_length = 50)
    DID = models.CharField(max_length = 50)
    content = models.TextField()
    date = models.DateTimeField('message time')
    def __str__(self):
        return self.SID + ',' + self.RID + ',' + self.content

#question
class Question(models.Model):
    QID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    question = models.TextField()
    answer = models.TextField()
    CID = models.CharField(max_length = 50)
    UID = models.CharField(max_length = 50)
    def __str__(self):
        return self.question + ',' + self.answer