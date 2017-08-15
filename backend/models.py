from django.db import models

# Create your models here.

class Enterprise(models.Model):
    '''
    企业表
    **属性**：
    * EID(String)：企业ID号，
    * name为企业名字，robot_icon为企业机器人头像，
    robot_name为企业机器人名字，state为企业状态（0为未激活，1为激活），chatbox_type
    为企业选择的窗口类型（1为嵌入式，2为窗口式，3为移动端），robot_state为企业机器人状态
    （0为未激活，1为激活）
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
    客服表，CID为客服ID号，EID为客服所在企业的ID号，icon为客服头像，name为客服昵称，
    state为客服状态（-1为注销，0为未激活，1为激活，2为在线，3为离线），service_number为正在服务
    的人数，service_number为服务过的人数，last_login为在最后一次登录的时间
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
    客户表，UID为客户ID，info为用户信息
    '''
    UID = models.CharField(max_length = 50, primary_key = True)
    info = models.CharField(max_length = 100)
    # class Meta:
    #     app_label = 'User'

class Dialog(models.Model):
    '''
    对话表，DID为本次对话的ID，EID为本次对话所属企业的ID，start_time为对话开始时间，
    end_time为对话结束时间，UID为用户ID，CID为客服ID，feedback为对话评分
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
    消息表，MID为本条消息的ID，SID为发送者ID，RID为接收者ID，DID为消息所属对话ID，
    content为消息内容，date为消息发送时间
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
    机器人问题表，QID为问题ID，EID为问题所属企业ID，category为问题所属目录
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
