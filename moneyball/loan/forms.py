# -*- coding: utf-8 -*- 
from django import forms
import datetime
from moneyball.common import widgets
from django.forms.extras.widgets import SelectDateWidget
from moneyball.loan.models import *
class LoanForm(forms.Form):
    loaddate = forms.DateField(label=u'日期', initial=datetime.date.today(), widget=SelectDateWidget())
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
        
    def save(self, instance=None):
        # Check the instance we've been given (if any)
        if instance is None:
            la = Loan()
        elif isinstance(instance, Loan):
            la = instance
        else:
            raise TypeError("instance is not a Loan")
        la.user = self.user
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
        
        la.save()
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
