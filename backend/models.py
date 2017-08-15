from django.db import models

# Create your models here.

class Enterprise(models.Model):
    '''企业'''
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
    class Meta:
        app_label = 'Enterprise'
    def __str__(self):
        return self.email + ',' + self.name

class Customer(models.Model):
    #customer
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
    class Meta:
        app_label = 'Customer'
    def __str__(self):
        return self.email + ',' + self.name

class User(models.Model):
    #user
    UID = models.CharField(max_length = 50, primary_key = True)
    info = models.CharField(max_length = 100)
    class Meta:
        app_label = 'User'

class Dialog(models.Model):
    #dialog
    DID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    UID = models.CharField(max_length = 50)
    CID = models.CharField(max_length = 50)
    feedback = models.IntegerField(default = 0)
    class Meta:
        app_label = 'Dialog'

class Message(models.Model):
    #messages
    MID = models.CharField(max_length = 50, primary_key = True)
    SID = models.CharField(max_length = 50)
    RID = models.CharField(max_length = 50)
    DID = models.CharField(max_length = 50)
    content = models.TextField()
    date = models.DateTimeField('message time')
    class Meta:
        app_label = 'Message'
    def __str__(self):
        return self.SID + ',' + self.RID + ',' + self.content

class Question(models.Model):
    #question
    QID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length = 50, default = 'unclassified')
    class Meta:
        app_label = 'Question'
    def __str__(self):
        return self.question + ',' + self.answer
