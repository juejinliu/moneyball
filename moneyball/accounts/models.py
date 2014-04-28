# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# 账户类型代码表
# 101:现金账户
# 102：银行卡存折
# 103：信用卡
# 104：电子账户
# 105：投资账户
class Orgtype(models.Model):
    type = models.IntegerField(default=1,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

# 金融机构代码表
class Orginfo(models.Model):
    code = models.CharField(max_length=10,unique=True)
    type = models.ForeignKey(Orgtype)
    name = models.CharField(max_length=150)
    def __unicode__(self):
        return unicode(self.name)
# 账户状态代码
class Accountstatus(models.Model):
    status = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)
    
# 账户信息
class Account(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    org = models.ForeignKey(Orginfo)
    type = models.ForeignKey(Orgtype)
    debitamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)    #信用额度
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    insrate = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=5,default=0.00)
    insratetype = models.IntegerField(blank=True,null=True,default=0)    #0-年利率 1-月利率 2-日利率
    insdate = models.DateField(blank=True,null=True,auto_now_add=False)  #结息日
    status = models.ForeignKey(Accountstatus)    #0-无效1-正常
    billdate = models.CharField(blank=True,null=True,max_length=2,default='00')  #账单日
    duedate = models.CharField(blank=True,null=True,max_length=2,default='00')  #还款日
    comments = models.CharField(blank=True,null=True,max_length=300)
    def __unicode__(self):
        return unicode(self.name)

# 账户月度余额
class Monthaccount(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    month = models.CharField(max_length=6)     #yyyymm
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    def __unicode__(self):
        return unicode(self.month)
        
# 交易类型代码
# 1-支出
# 2-收入
# 3-转账
# 4-借款报销
# 5-信用卡还款
class Transtype(models.Model):
    type = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

# 全局交易代码 跟用户无关
class Transcode(models.Model):
    type = models.ForeignKey(Transtype)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

# 用户自定义交易代码,用户注册时从Transcode表中复制过来
class Usertranscode(models.Model):
    user = models.ForeignKey(User)
    type = models.ForeignKey(Transtype)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

class Trancations(models.Model):
    user = models.ForeignKey(User)
    source = models.ForeignKey(Account,blank=True,null=True, related_name='source')
    target = models.ForeignKey(Account, related_name='target')
    transcode = models.ForeignKey(Usertranscode)
    amount = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    comments = models.CharField(blank=True,null=True,max_length=300)
    def __unicode__(self):
        return unicode(self.target)


