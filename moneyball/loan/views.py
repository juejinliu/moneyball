# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from moneyball.loan.forms import LoanForm,PlatformForm
# Create your views here.
def loaninfo(request):
    if request.method == 'POST':
        form = LoanForm(request.user, request.POST)
        if form.is_valid():
            new_loan = form.save()
            return render_to_response("success.html",({'infomsg':u'添加成功'}), RequestContext(request))
        else:
            pass
    else:
        form = LoanForm(request.user)
    return render_to_response("loan.html", {'form': form}, RequestContext(request))

def platforminfo(request):
    if request.method == 'POST':
        form = PlatformForm(request.POST)
        if form.is_valid():
            new_platform = form.save(request)
            return render_to_response("success.html",{'infomsg':u'添加成功'}, RequestContext(request))
        else:
            pass
    else:
        form = PlatformForm()
    return render_to_response("platform.html", {'form': form}, RequestContext(request))

