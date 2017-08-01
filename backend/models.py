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
	def __str__(self):
		return self.email + ',' + self.name

#customer
class Customer(models.Model):
	CID = models.CharField(max_length=50, primary_key=True)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=50)
	icon = models.CharField(max_length=50)
	name = models.CharField(max_length=10)
	EID = models.ForeignKey(Enterprise)
	state = models.IntegerField(default=0)
	service_number = models.IntegerField(default=0)
	last_login = models.DateField()
	salt = models.CharField(max_length=8)
	def __str__(self):
		return self.email + ',' + self.name

#user
class User(models.Model):
	UID = models.CharField(max_length=50)

#messages
class Message(models.Model):
	SID = models.CharField(max_length=50)
	RID = models.CharField(max_length=50)
	content = models.TextField()
	date = models.DateField()