# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from moneyball.user.models import MyUser
from django.template.loader import render_to_string

class Booleancode(models.Model):
    code = models.IntegerField(default=1,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

class Returntype(models.Model):
    type = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

class Returnstatus(models.Model):
    status = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)

class Platform(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    platformurl = models.URLField(blank=True,null=True)
    rate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    active = models.ForeignKey(Booleancode,default=2)
    onlinetime = models.DateField(auto_now_add=True)
    delegaterate = models.DecimalField(decimal_places=2,max_digits=5,default=0.00)
    def __unicode__(self):
        return unicode(self.name)

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
    loandate = models.DateField(auto_now_add=False)
    returntype = models.ForeignKey(Returntype)    #'1':'等额本息','2':'月还息到期还本','3':'到期还本息'
    status = models.ForeignKey(Returnstatus)    #0-正在还款1-已还款2-已坏账,未赔付3-坏账已赔付
    awardamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    insamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    continuedamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    feeamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    offlineamt = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    returndate = models.DateField(blank=True,null=True)
    comments = models.CharField(blank=True,null=True,max_length=300)
#     oldid = models.IntegerField()   #用于更新导入数据，正常情况不需要这个字段
            
    def __unicode__(self):
        return unicode(self.user)
    
    def enrollment_chart(self):
        lu = { 'categories' : [ 'Fall 2008', 'Spring 2009','Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011'],\
             'undergrad' : [18, 22, 30, 34, 40, 47],\
             'grad' : [1, 2, 4, 4, 5, 7],\
             'employee' : [2, 3, 0, 1, 1, 2] }
        lu['total_enrolled'] = [sum(a) for a in zip(lu['undergrad'], lu['grad'],lu['employee'])]
        return render_to_string('admin/loan/loan/enrollment_chart.html', lu )
    enrollment_chart.allow_tags = True                    

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
    loandate = models.DateField(auto_now_add=False)
    expiredate = models.DateField(auto_now_add=False)
    status = models.ForeignKey(Returnstatus)    #0-正在还款1-已还款2-已坏账,未赔付3-坏账已赔付
    returndate = models.DateField(blank=True,null=True)             #回款日期
    latecharge = models.DecimalField(decimal_places=2,max_digits=9,default=0.00)
    comments = models.CharField(blank=True,null=True,max_length=300)
    def __unicode__(self):
        return unicode(self.feeamt)


