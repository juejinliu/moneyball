# -*- coding: utf-8 -*- 
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User)
    wxid = models.CharField(blank=True,null=True,max_length=50)
    dob = models.DateField(blank=True,null=True)
    mobile = models.CharField(blank=True,null=True,max_length=20)
    def __unicode__(self):
        return unicode(self.user.username)
