from django.db import models
# from django import forms
#
# # Create your models here.
#
#
# class Test(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     phone = models.IntegerField()
#     user = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#
#
# class Session(models.Model):
#     sessionID = models.ForeignKey(
#         'UserDetails',
#         on_delete=models.CASCADE,
#     )
#     sessionIn = models.CharField(max_length=15)
#     sessionOut = models.CharField(max_length=15)
#     sessionStat = models.IntegerField()
#
#
# class UserDetails(models.Model):
#     adminID = models.AutoField(primary_key=True)
#     adminName = models.CharField(max_length=50)
#     adminEmail = models.CharField(max_length=50)
#     adminPhone = models.CharField(max_length=11)
#     adminUser = models.CharField(max_length=50)
#     adminPass = models.CharField(max_length=100)
#     adminRole = models.CharField(max_length=40)
#     adminStatus = models.IntegerField()
#     adminDT = models.DateTimeField(auto_now=True)
#     adminRef = models.CharField(max_length=20)
#     adminPerms = models.IntegerField()