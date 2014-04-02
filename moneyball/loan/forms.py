# -*- coding: utf-8 -*- 
from django import forms
import datetime,time
from moneyball.common.utilfun import addmonths
from moneyball.common import widgets
from django.forms.extras.widgets import SelectDateWidget
from moneyball.loan.models import *
import math
class LoanForm(forms.Form):
    loandate = forms.DateField(label=u'日期', initial=datetime.date.today(), widget=SelectDateWidget())
    platform = forms.ModelChoiceField(label=u'平台',queryset=None)
    amount = forms.DecimalField(label=u'金额', initial='0')
    RETURNCHOICES = (('1', u'等额本息',),('2', u'月还息到期还本',), ('3', '到期还本息',))     #'1':'等额本息','2':'月还息到期还本','3':'到期还本息'
    returntype = forms.ChoiceField(label=u'还款方式', choices=RETURNCHOICES)
    duration = forms.IntegerField(label=u'借款期限', initial='1')
    DURATIONCHOICES = (('0', u'月',),('1', u'天',))     #
    daily = forms.ChoiceField(label=u'', initial='0', widget=forms.RadioSelect, choices=DURATIONCHOICES)
    RATETYPECHOICES = (('0', u'年利率',),('1', u'日利率',))     #
    insratetype = forms.ChoiceField(label=u'利率类型', choices=RATETYPECHOICES)
    insrate = forms.DecimalField(label=u'利率', initial='0.00' )
    continuerate = forms.DecimalField(label=u'续投奖励', initial='0.00' )
    awardrate = forms.DecimalField(label=u'投标奖励', initial='0.00' )
    feerate = forms.DecimalField(label=u'手续费', initial='0.00' )
    offlinerate = forms.DecimalField(label=u'线下充值奖励', initial='0.00')
    comments =  forms.CharField(label=u'备注', widget=forms.Textarea(),required=False)
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(LoanForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Platform.objects.filter(user=self.user).order_by('name')
    
    def calinsamt(self, instance=None):
        if instance is None:
            la = Loan()
        elif isinstance(instance, Loan):
            la = instance
        else:
            raise TypeError("instance is not a Loan")
        if la.insratetype == '0':   #年利率
            insrate = la.insrate
        elif la.insratetype == '1':     #月利率
            insrate = la.insrate * 12
        else:
            insrate = la.insrate * 365  #日利率
        
        if la.daily == '0' and la.seconds == 0:
            if la.returntype == '0':    #等额本金
                divAmt = la.amount / la.duration
                remainAmt = la.amount
                for i in range(0,la.duration):
                    la.insamt += remainAmt * insrate / 1200
                    remainAmt -= divAmt
            elif la.returntype == '1':  #等额本息
                monthactive = insrate / 1200
                totalmoney = la.amount
                totalmonth = la.duration
                la.insamt = 0
                for i in range(0,totalmonth):
                    monthinterestmoney = totalmoney * monthactive * (pow((1+monthactive),totalmonth)-pow((1+monthactive),i))/(pow((1+monthactive),totalmonth)-1);
                    la.insamt += monthinterestmoney;
            elif la.returntype == '2' or la.returntype == '3':
                la.insamt = la.amount * la.duration / 12 * insrate / 100
        if la.daily == '1' and la.seconds == 0:
            la.insamt = la.amount * la.duration / 365 * insrate / 100
        return la.insamt
    #插入待收明细
    def insert_detail(self, instance=None):
        """
        split loan record to detail records
        
        Arguments:
        """
        if instance is None:
            la = Loan()
        elif isinstance(instance, Loan):
            la = instance
        else:
            raise TypeError("instance is not a LoanDetail")
        
        if (la.insratetype == '0'):     #年利率
            insrate = la.insrate;
        elif (la.insratetype == '1'):   #月利率
            insrate = la.insamt * 12
        else:    #日利率
            insrate = la.insamt * 365
        
        loandtl = Loandetail()
        loandtl.loan = la
        loandtl.user = la.user
        loandtl.platform = la.platform
        loandtl.totalperiod = la.duration
        loandtl.status = 0
        loandtl.insrate = la.insrate
        loandtl.loandate = la.loandate
        if (la.daily == '0'):           #月标
            if la.returntype == '0':    #等额本金
                remainAmt = la.amount
                divAmt = la.amount / la.duration
                for i in range(0,la.duration):
                    loandtl.period = i+1
                    loandtl.insamt = remainAmt * insrate / 1200
                    loandtl.ownamt = divamt
                    loandtl.feeamt = loandtl.insamt * la.feerate / 100
                    loandtl.expiredate = addmonths(la.loandate,1+1,False)
                    remainAmt -= divAmt
                    loandtl.save(force_insert=True)
                    loandtl.id=None
            if la.returntype == '1':    #等额本息
                monthactive = insrate / 1200
                totalmoney = la.amount
                totalmonth = la.duration
                monthmoney = totalmoney*monthactive*(pow((1+monthactive),totalmonth))/(pow((1+monthactive),totalmonth)-1)   #每月还款额
                for i in range(0,la.duration):
                    monthinterestmoney = totalmoney*monthactive*(pow((1+monthactive),totalmonth)-pow((1+monthactive),i))/(pow((1+monthactive),totalmonth)-1)    #每月利息额
                    principalmoney = monthmoney-monthinterestmoney  #每月本金
                    loandtl.ownamt = principalmoney
                    loandtl.period = i+1
                    loandtl.insamt = monthinterestmoney
                    loandtl.feeamt = monthinterestmoney * la.feerate / 100
                    loandtl.expiredate = addmonths(la.loandate,i+1,False)
                    loandtl.save(force_insert=True)
                    loandtl.id=None
            if la.returntype == '2':    #月还息到期还本
                loandtl.insamt = la.amount * insrate / 1200
                loandtl.feeamt = loandtl.insamt * la.feerate / 100
                for i in range(0,la.duration):
                    loandtl.period = i+1
                    loandtl.expiredate = addmonths(la.loandate,i+1,False)
                    if i == la.duration - 1:
                        loandtl.ownamt = la.amount
                    else:
                        loandtl.ownamt = 0
                    loandtl.save(force_insert=True)
                    loandtl.id=None
            if la.returntype == '3':
                loandtl.insamt = la.amount * la.duration * insrate / 1200
                loandtl.feeamt = loandtl.insamt * la.feerate / 100
                loandtl.period = 1
                loandtl.ownamt = la.amount
                loandtl.expiredate = addmonths(la.loandate,la.duration,False)
                loandtl.save(force_insert=True)
        if la.daily == '1':      #天标--仅支持到期还本息
            loandtl.insamt = la.amount * la.duration /360 * insrate /100;  #计算总共的利息
            loandtl.feeamt = loandtl.insamt * la.feerate / 100
            loandtl.period = 1
            loandtl.ownamt = la.amount
            loandtl.expiredate = la.loandate + datetime.timedelta(days=la.duration)
            loandtl.save(force_insert=True)
    ##############################################
    def save(self, instance=None):
        # Check the instance we've been given (if any)
        if instance is None:
            la = Loan()
        elif isinstance(instance, Loan):
            la = instance
        else:
            raise TypeError("instance is not a Loan")
        la.user = self.user
        la.loandate = self.cleaned_data['loandate']
        la.platform = self.cleaned_data['platform']
        la.amount = self.cleaned_data['amount']
        la.returntype = self.cleaned_data['returntype']
        la.duration = self.cleaned_data['duration']
        la.daily = self.cleaned_data['daily']
        la.insratetype = self.cleaned_data['insratetype']
        la.insrate = self.cleaned_data['insrate']
        la.continuerate = self.cleaned_data['continuerate']
        la.awardrate = self.cleaned_data['awardrate']
        la.feerate = self.cleaned_data['feerate']
        la.offlinerate = self.cleaned_data['offlinerate']
        la.comments = self.cleaned_data['comments']
        ######################计算数据
        la.status = 0
        la.awardamt = la.amount * la.awardrate / 100
        la.insamt = self.calinsamt(la)
        la.continuedamt = la.amount * la.continuerate / 100
        la.feeamt = la.insamt * la.feerate / 100
        la.offlineamt = la.amount * la.offlinerate / 100
        if la.daily == '0':   #月标
            la.returndate = addmonths(la.loandate,la.duration,False)
        elif la.daily == '1': #天标
            la.returndate = datetime.datetime.now() + datetime.timedelta(days = la.duration)
        la.save()
        #####################插入明细
        self.insert_detail(la)
        return la


class PlatformForm(forms.Form):
    name = forms.CharField(label=u'名称(必填)', max_length=50)
    platfromurl = forms.URLField(label=u'网址', required=False,initial='http://')
    rate = forms.DecimalField(label=u'管理费率', initial='0.00')
    delegaterate = forms.DecimalField(label=u'代理人费率', initial='0.00')
    onlinetime = forms.DateField(label=u'上线日期', initial=datetime.date.today(), widget=SelectDateWidget())
    active = forms.ChoiceField(label=u'状态', widget=forms.RadioSelect, choices=[(1, u'正常'), (0, u'隐藏')], initial='1')
    error_css_class = 'error'
    required_css_class = 'required'
    def save(self, request , instance=None):
        # Check the instance we've been given (if any)
        if instance is None:
            pf = Platform()
        elif isinstance(instance, Platform):
            pf = instance
        else:
            raise TypeError("instance is not a Platform")
        pf.user = request.user
        pf.name = self.cleaned_data['name']
        pf.platfromurl = self.cleaned_data['platfromurl']
        pf.rate = self.cleaned_data['rate']
        pf.delegaterate = self.cleaned_data['delegaterate']
        pf.onlinetime = self.cleaned_data['onlinetime']
        pf.active = self.cleaned_data['active']
        pf.save()
        return pf
