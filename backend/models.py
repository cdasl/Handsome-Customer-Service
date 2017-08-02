from django.db import models

# Create your models here.

#enterprise
class Enterprise(models.Model):
    EID = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    robot_icon = models.CharField(max_length=50)
    robot_name = models.CharField(max_length=10)
    state = models.IntegerField(default=0)
    salt = models.CharField(max_length=8)
    chatbox_type = models.IntegerField(default=1)
    def __str__(self):
        return self.email + ',' + self.name

#customer
class Customer(models.Model):
    CID = models.CharField(max_length=50, primary_key=True)
    EID = models.ForeignKey(Enterprise)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    name = models.CharField(max_length=10)
    state = models.IntegerField(default=0)
    service_number = models.IntegerField(default=0)
    serviced_number = models.IntegerField(default=0)
    last_login = models.DateField()
    salt = models.CharField(max_length=8)
    def __str__(self):
        return self.email + ',' + self.name

#user
class User(models.Model):
    UID = models.CharField(max_length=50)
    info = models.TextField(max_length=500)

#dialog
class Dialog(models.Model):
    DID = models.CharField(max_length=50, primary_key=True)
    EID = models.ForeignKey(Enterprise)
    start_time = models.DateTimeField('start time', auto_now=True)
    end_time = models.DateTimeField('end time', auto_now=True)

#messages
class Message(models.Model):
    MID = models.CharField(max_length=50)
    SID = models.CharField(max_length=50)
    RID = models.CharField(max_length=50)
    DID = models.ForeignKey(Dialog)
    content = models.TextField()
    date = models.DateTimeField('message time', auto_now = True)
    def __str__(self):
        return self.SID + ',' + self.RID + ',' + self.content

#question
class Question(models.Model):
    QID = models.CharField(max_length=50, primary_key=True)
    EID = models.ForeignKey(Enterprise)
    question = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return self.question + ',' + self.answer