# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from moneyball.loan.models import *
from django.db.models import Sum
# Create your views here.
def index(request):
    return render_to_response('index.html')

@login_required
def welcome(request):
    tempstatus = Returnstatus.objects.get(status = 0)
    today_due_list = Loandetail.objects.filter(user=request.user,status=tempstatus).order_by('expiredate')
    amount_sum = 0.00
    if today_due_list and today_due_list.count > 0:
        amount_sum = today_due_list.aggregate(Sum('ownamt'))['ownamt__sum']
        amount_sum += today_due_list.aggregate(Sum('insamt'))['insamt__sum']
        amount_sum -= today_due_list.aggregate(Sum('feeamt'))['feeamt__sum']
    return render_to_response('welcome.html', {"today_due_list": today_due_list,
                                               "record_number": today_due_list.count,
                                               "amount_sum":amount_sum,}, RequestContext(request))

def wxfocus(request):
    return render_to_response('overall_template.html')


def logout(request):
    auth.logout(request)
    return render_to_response("login.html")
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/welcome')
            #return render_to_response('welcome.html', {"today_due_list": today_due_list}, RequestContext(request))
            #return render_to_response("welcome.html", RequestContext(request))
        else:
            # Show an error page
            return render_to_response("login.html",({'errormsg':u'用户名或密码错误'}), RequestContext(request))
    else:
        return render_to_response("login.html", RequestContext(request))