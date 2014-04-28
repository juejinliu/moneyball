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
    billdate = forms.CharField(label=u'账单日', max_length=2)
    duedate = forms.CharField(label=u'还款日', max_length=2)
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

