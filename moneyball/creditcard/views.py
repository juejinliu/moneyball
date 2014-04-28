# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from moneyball.creditcard.forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from moneyball.creditcard.models import *
from moneyball.accounts.models import *
# from graphos.sources.model import ModelDataSource
# from graphos.renderers import flot
from django.template.loader import render_to_string
from moneyball.loan.loancalc import * 
import json
import datetime
# Create your views here.
def index(request):
    pass


#===============================================================================
# 信用卡的修改，隐藏，添加操作在这个类里面全部完成
#===============================================================================
@login_required
def creditcardinfo(request,ccid=None,status=None):
    form = CreditcardForm(Account())
    creditcardid = ccid
    if request.method == 'POST':
        form = CreditcardForm(None,request.POST)
        if form.is_valid():
            #try:
            new_Creditcard = form.save(request,None,ccid)
            #except:
            #    raise Http404
    elif request.method == 'GET':
        try:
            if ccid:
                rtn_record = Account.objects.get(id=ccid)
                if status:
                    status_record = Accountstatus.objects.get(status=status)
                    rtn_record.status = status_record
                    rtn_record.save()
                else:
                    form = CreditcardForm(rtn_record)
                    creditcardid = rtn_record.id
        except Creditcard.DoesNotExist:
            return render_to_response("success.html",({'errormsg':u'不存在这条记录'}), RequestContext(request))
    results = Account.objects.filter(user=request.user).order_by('id')
    return render_to_response("Creditcard.html", RequestContext(request,{
                                                'form': form,
                                                'id': creditcardid,
                                                'infomsg':u'操作成功',
                                                "creditcard_list": results})
                                  )

