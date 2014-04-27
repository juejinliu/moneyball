# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from moneyball.accounts.models import *
from django.template.loader import render_to_string

# 信用卡账单表
class Billinfo(models.Model):
    account = models.ForeignKey(Account)
    amount = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #账单金额
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #当前余额
    billmonth = models.CharField(max_length=6)
    dueday = models.DateField(auto_now_add=False)  #到期日
    splitpay = models.IntegerField(default=0)    #0-不分期 1-分期
    splitpaynum = models.IntegerField(default=0)    #分期期数
    splitrate = models.IntegerField(default=0)    #分期费率
    minpay = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #最低还款额
    def __unicode__(self):
        return unicode(self.account)
    
# # 信用卡账单明细表
# class Billdtlinfo(models.Model):
#     account = models.ForeignKey(Account)
#     def __unicode__(self):
#         return unicode(self.account)    

