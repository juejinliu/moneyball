# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class Wxautoreply(models.Model):
    code = models.CharField(max_length=50,unique=True)
    content = models.CharField(max_length=1000)
    def __unicode__(self):
        return unicode(self.code)