from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class UserDetails(AbstractBaseUser):
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    token = models.CharField(max_length=100)
    role = models.CharField(max_length=40)
    status = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    ref = models.CharField(default=None, max_length=20)
    perms = models.IntegerField()
    team = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def addtoDB(self, user, passw, phone, email):
        add = UserDetails(username=user, password=passw, phone=phone, email=email)
        add.save()

    def delete_everything(self):
        UserDetails.objects.all().delete()

class ResetTokens(models.Model):
    token = models.CharField(max_length=40)
    time = models.DateTimeField()
    status = models.BooleanField(max_length=0)

class Details(models.Model):
    requestId = models.AutoField(primary_key=True)
    uid = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.TextField()
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.BooleanField(default=False)
    approve = models.IntegerField(default=0)
    disapprove = models.IntegerField(default=0)
    remark = models.TextField(default=None, blank=True)
    admin1 = models.CharField(max_length=150)