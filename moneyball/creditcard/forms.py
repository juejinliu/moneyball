# -*- coding: utf-8 -*- 
from django import forms
import datetime,time
from moneyball.common.utilfun import addmonths
from moneyball.common import widgets
from django.forms.extras.widgets import SelectDateWidget
from moneyball.creditcard.models import *
from moneyball.accounts.models import *
import math
from django.db.models import Q
from simple_search import BaseSearchForm
 
class CreditcardForm(forms.Form):
    name = forms.CharField(label=u'名称(必填)', max_length=50)
    org = forms.ModelChoiceField(label=u'开户机构', queryset=None)
    debitamt = forms.DecimalField(label=u'信用额度', initial='0')
    balance = forms.DecimalField(label=u'目前欠款', initial='0')
    billdate = forms.CharField(label=u'账单日', max_length=2, initial='01')
    duedate = forms.CharField(label=u'还款日', max_length=2, initial='18')
    status = forms.ModelChoiceField(label=u'状态', widget=forms.RadioSelect,queryset=Accountstatus.objects.all().order_by('-status'),initial=2)
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, data, *args, **kwargs):
        super(CreditcardForm, self).__init__(*args, **kwargs)
        cc_orgtype = Orgtype.objects.get(type='103')
        self.fields['org'].queryset = Orginfo.objects.filter(type=cc_orgtype).order_by('name')
        if data:
            if isinstance(data, Account) and data.name:
                self.fields['name'].initial = data.name
                self.fields['org'].initial = data.org
                self.fields['debitamt'].initial = data.debitamt
                self.fields['balance'].initial = data.balance
                self.fields['billdate'].initial = data.billdate
                self.fields['duedate'].initial = data.duedate
                self.fields['status'].initial = data.status
    def save(self, request , instance=None, id=None):
        # Check the instance we've been given (if any)
        if instance is None:
            cc = Account()
        elif isinstance(instance, Account):
            cc = instance
        else:
            raise TypeError("instance is not a Creditcard")
        cc.id = id
        cc.user = request.user
        cc.type = Orgtype.objects.get(type='103')
        cc.name = self.cleaned_data['name']
        cc.org = self.cleaned_data['org']
        cc.debitamt = self.cleaned_data['debitamt']
        cc.balance = self.cleaned_data['balance']
        cc.billdate = self.cleaned_data['billdate']
        cc.duedate = self.cleaned_data['duedate']
        cc.status = self.cleaned_data['status']
        cc.save()
        return cc

#账单信息
class BillForm(forms.Form):
    acct = forms.ModelChoiceField(label=u'信用卡(必填)', queryset=None)
    amount = forms.DecimalField(label=u'本期账单金额', initial='0')
    balance = forms.DecimalField(label=u'当前余额', initial='0')
    billmonth = forms.ModelChoiceField(label=u'账单月份', queryset=Billmonth.objects.filter(status=1).order_by('month'))
    dueday = forms.DateField(label=u'最后还款日', initial=datetime.date.today(), widget=SelectDateWidget())
    splitamt = forms.DecimalField(label=u'分期金额', initial='0.00')
    splitpaynum = forms.DecimalField(label=u'分期期数', initial='0')
    splitrate = forms.DecimalField(label=u'分期费率', initial='0.00')
    minpay = forms.DecimalField(label=u'最低还款额', initial='0')
    paidamt = forms.DecimalField(label=u'已还金额', initial='0')
    status = forms.ModelChoiceField(label=u'状态', widget=forms.RadioSelect,queryset=Billstatus.objects.all().order_by('-status'),initial=1)
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, data, user, *args, **kwargs):
        self.user = user
        super(BillForm, self).__init__(*args, **kwargs)
        cc_orgtype = Orgtype.objects.get(type='103')
        cc_status = Accountstatus.objects.get(status=1)
        self.fields['acct'].queryset = Account.objects.filter(user=self.user,type=cc_orgtype,status=cc_status).order_by('name')
        if data:
#             if isinstance(data, Billinfo) and data.account:
            if isinstance(data, Billinfo):
                self.fields['acct'].initial = data.acct
                self.fields['amount'].initial = data.amount
                self.fields['balance'].initial = data.balance
                self.fields['billmonth'].initial = data.billmonth
                self.fields['dueday'].initial = data.dueday
                self.fields['splitamt'].initial = data.splitamt
                self.fields['splitpaynum'].initial = data.splitpaynum
                self.fields['splitrate'].initial = data.splitrate
                self.fields['minpay'].initial = data.minpay
                self.fields['paidamt'].initial = data.paidamt
                self.fields['status'].initial = data.status
    def save(self, request , instance=None, id=None):
        # Check the instance we've been given (if any)
        if instance is None:
            bi = Billinfo()
        elif isinstance(instance, Billinfo):
            bi = instance
        else:
            raise TypeError("instance is not a Billinfo")
        bi.id = id
        bi.user = request.user
        bi.acct = self.cleaned_data['acct']
        bi.amount = self.cleaned_data['amount']
        bi.balance = self.cleaned_data['balance']
        bi.billmonth = self.cleaned_data['billmonth']
        bi.dueday = self.cleaned_data['dueday']
        bi.splitamt = self.cleaned_data['splitamt']
        bi.splitpaynum = self.cleaned_data['splitpaynum']
        bi.splitrate = self.cleaned_data['splitrate']
        bi.minpay = self.cleaned_data['minpay']
        bi.paidamt = self.cleaned_data['paidamt']
        
        bi.status = self.cleaned_data['status']
        bi.save()
        return bi
    
#账单还款信息
class BillpayForm(forms.Form):
    target = forms.ModelChoiceField(label=u'信用卡', queryset=None)
    source = forms.ModelChoiceField(label=u'转出账户', queryset=None)
    amount = forms.DecimalField(label=u'还款金额', initial='0')
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, data, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        cc_orgtype = Orgtype.objects.get(type='103')
        cc_status = Accountstatus.objects.get(status=1)
        self.fields['acct'].queryset = Account.objects.filter(type=cc_orgtype,status=cc_status).order_by('name')
        if data:
#             if isinstance(data, Billinfo) and data.account:
            if isinstance(data, Billinfo):
                self.fields['acct'].initial = data.acct
                self.fields['amount'].initial = data.amount
                self.fields['balance'].initial = data.balance
                self.fields['billmonth'].initial = data.billmonth
                self.fields['dueday'].initial = data.dueday
                self.fields['splitamt'].initial = data.splitamt
                self.fields['splitpaynum'].initial = data.splitpaynum
                self.fields['splitrate'].initial = data.splitrate
                self.fields['minpay'].initial = data.minpay
                self.fields['paidamt'].initial = data.paidamt
                self.fields['status'].initial = data.status
    def save(self, request , instance=None, id=None):
        # Check the instance we've been given (if any)
        if instance is None:
            bi = Billinfo()
        elif isinstance(instance, Billinfo):
            bi = instance
        else:
            raise TypeError("instance is not a Billinfo")
        bi.id = id
        bi.user = request.user
        bi.acct = self.cleaned_data['acct']
        bi.amount = self.cleaned_data['amount']
        bi.balance = self.cleaned_data['balance']
        bi.billmonth = self.cleaned_data['billmonth']
        bi.dueday = self.cleaned_data['dueday']
        bi.splitamt = self.cleaned_data['splitamt']
        bi.splitpaynum = self.cleaned_data['splitpaynum']
        bi.splitrate = self.cleaned_data['splitrate']
        bi.minpay = self.cleaned_data['minpay']
        bi.paidamt = self.cleaned_data['paidamt']
        
        bi.status = self.cleaned_data['status']
        bi.save()
        return bi
