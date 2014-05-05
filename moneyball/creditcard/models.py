# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from moneyball.accounts.models import *
from django.template.loader import render_to_string

# 信用卡账单状态代码
# 0 - 未还款
# 1 - 还部分
# 2 - 已还清
class Billstatus(models.Model):
    status = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return unicode(self.name)

class Billmonth(models.Model):
    month = models.CharField(max_length=6,unique=True)
    status = models.IntegerField(default=1)   #1-有效 0-无效
    def __unicode__(self):
        return unicode(self.month)

# 信用卡账单表
class Billinfo(models.Model):
    user = models.ForeignKey(User)
    acct = models.ForeignKey(Account)
    amount = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #账单金额
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #当前余额
    billmonth = models.ForeignKey(Billmonth)
    dueday = models.DateField(auto_now_add=False)  #到期日
    splitamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)    #分期金额
    splitpaynum = models.IntegerField(default=0)    #分期期数
    splitrate = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)    #分期费率
    minpay = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)   #最低还款额
    status = models.ForeignKey(Billstatus)    #
    def __unicode__(self):
        return unicode(self.amount)
    
# # 信用卡账单明细表
# class Billdtlinfo(models.Model):
#     account = models.ForeignKey(Account)
#     def __unicode__(self):
#         return unicode(self.account)    

