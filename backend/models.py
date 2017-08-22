from django.db import models

# Create your models here.

class Enterprise(models.Model):
    '''
    企业表\n
    * EID(String)：企业ID\n
    * name(String)：企业名字\n
    * robot_icon(String)：企业机器人头像，储存路径\n
    * robot_name(String)：企业机器人名字\n
    * state(int)：企业状态（0：未激活，1：激活）\n
    * chatbox_type(int)：企业选择的窗口类型（1：嵌入式，2：窗口式，3：移动端）\n
    * robot_state(int)：企业机器人状态（0：未激活，1：激活）\n
    '''
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
    # class Meta:
    #     app_label = 'Enterprise'
    def __str__(self):
        return self.email + ',' + self.name

class Customer(models.Model):
    '''
    客服表\n
    * CID(String)：客服ID\n
    * EID(String)：客服所在企业ID\n
    * name(String)：客服昵称\n
    * state(int)：客服状态（-1：注销，0：未激活，1：激活，2：休息，3：工作）\n
    * service_number(int)：客服正在服务的人数\n
    * serviced_number(int)：客服服务过的人数\n
    * last_login(date)：客服最后一次登录的时间\n
    '''
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
    # class Meta:
    #     app_label = 'Customer'
    def __str__(self):
        return self.email + ',' + self.name

class User(models.Model):
    '''
    用户表\n
    * UID(String)：客户ID\n
    * info(String)：用户信息\n
    '''
    UID = models.CharField(max_length = 50, primary_key = True)
    info = models.CharField(max_length = 100)
    # class Meta:
    #     app_label = 'User'

class Dialog(models.Model):
    '''
    对话表\n
    * DID(String)：本次对话的ID\n
    * EID(String)：本次对话所属企业的ID\n
    * start_time(date)：对话开始时间\n
    * end_time(date)：对话结束时间\n
    * UID(String)：用户ID\n
    * CID(String)：客服ID\n
    * feedback(int)：对话评分\n
    '''
    DID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    UID = models.CharField(max_length = 50)
    CID = models.CharField(max_length = 50)
    feedback = models.IntegerField(default = 0)
    # class Meta:
    #     app_label = 'Dialog'

class Message(models.Model):
    '''
    消息表\n
    * MID(String)：本条消息的ID\n
    * SID(String)：发送者ID\n
    * RID(String)：接收者ID\n
    * DID(String)：消息所属对话ID\n
    * content(String)：消息内容\n
    * date(date)：消息发送时间\n
    '''
    MID = models.CharField(max_length = 50, primary_key = True)
    SID = models.CharField(max_length = 50)
    RID = models.CharField(max_length = 50)
    DID = models.CharField(max_length = 50)
    content = models.TextField()
    date = models.DateTimeField('message time')
    # class Meta:
    #     app_label = 'Message'
    def __str__(self):
        return self.SID + ',' + self.RID + ',' + self.content

class Question(models.Model):
    '''
    机器人问题表\n
    * QID(String)：问题ID\n
    * EID(String)：问题所属企业ID\n
    * category(String)：问题所属目录\n
    '''
    QID = models.CharField(max_length = 50, primary_key = True)
    EID = models.CharField(max_length = 50)
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length = 50, default = 'unclassified')
    # class Meta:
    #     app_label = 'Question'
    def __str__(self):
        return self.question + ',' + self.answer
