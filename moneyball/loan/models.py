# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
class Platform(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    platfromurl = models.URLField(blank=True,null=True)
    rate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    active = models.IntegerField(default=0)
    onlinetime = models.DateField(auto_now_add=True)
    delegaterate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    def __unicode__(self):
        return self.name

class Loan(models.Model):
    user = models.ForeignKey(User)
    platform = models.ForeignKey(Platform)
    amount = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    insrate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    insratetype = models.IntegerField(default=0)    #0-年利率 1-月利率 2-日利率
    awardrate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    continuerate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    offlinerate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    feerate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    daily = models.IntegerField(default=0)    #是否天标 0-no 1-yes
    seconds = models.IntegerField(default=0)    #是否秒标 0-no 1-yes
    duration = models.IntegerField(default=1)    #借出时长,默认是月数
    loantype = models.IntegerField(default=0)    #是否秒标 0-本人投标 1-下线投标
    delegaterate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)  #代理人佣金费率
    loaddate = models.DateTimeField(auto_now_add=True)
    returntype = models.IntegerField(default=1)    #'1':'等额本息','2':'月还息到期还本','3':'到期还本息'
    status = models.IntegerField(default=0)    #0-正在还款1-已还款2-已坏账,未赔付3-坏账已赔付
    awardamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    insamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    continuedamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    feeamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    offlineamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    returndate = models.DateField()
    comments = models.CharField(max_length=300)
            
    def __unicode__(self):
        return self.name
    
    def insert_detail(self):
        """
        split loan record to detail records
        
        Arguments:
        """
        if (self.insratetype == 0):     #年利率
            insrate = self.insrate;
        elif (self.insratetype == 1):   #月利率
            insrate = self.insamt * 12
        else:    #日利率
            insrate = self.insamt * 365
        
        if (self.daily == 0):           #月标
            if self.returntype == 0:    #等额本金
                for i in range(0,self.duration):
                    loandtl = Loandetail
                    loandtl.loan = self
                    loandtl.platform = self.platform
                    loandtl.period = i
                    loandtl.totalperiod = self.duration
                    loandtl.save()
                    
class Loandetail(models.Model):
    loan = models.ForeignKey(Loan)
    user = models.ForeignKey(User)
    platform = models.ForeignKey(Platform)
    period = models.IntegerField(default=1)    #当前期数
    totalperiod = models.IntegerField(default=0)    #总期数
    insamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    ownamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    feeamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    insrate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    loaddate = models.DateTimeField(auto_now_add=True)
    expiredate = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)    #0-正在还款1-已还款2-已坏账,未赔付3-坏账已赔付
    returndate = models.DateField()             #回款日期
    latecharge = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    comments = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name
