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
from moneyball.loan.loancalc import *
from locale import LC_ALL
# Create your views here.
def index(request):
    return render_to_response('index.html')

@login_required
def welcome(request):
#     global loan_notreturnstatus #待收状态
#     loan_notreturnstatus = Returnstatus.objects.get(status = 0)
#     today_due_list = Loandetail.objects.filter(user=request.user,status=loan_notreturnstatus).order_by('expiredate')
#     insamt_sum = 0.00
#     feeamt_sum = 0.00
#     ownamt_sum = 0.00
#     amount_sum = 0.00
#     if today_due_list and today_due_list.count > 0:
# #         amount_sum = today_due_list.aggregate(Sum('ownamt'))['ownamt__sum']
# #         amount_sum += today_due_list.aggregate(Sum('insamt'))['insamt__sum']
# #         amount_sum -= today_due_list.aggregate(Sum('feeamt'))['feeamt__sum']
#         insamt_sum = today_due_list.aggregate(Sum('insamt'))['insamt__sum']
#         ownamt_sum = today_due_list.aggregate(Sum('ownamt'))['ownamt__sum']
#         feeamt_sum = today_due_list.aggregate(Sum('feeamt'))['feeamt__sum']
#         amount_sum = ownamt_sum + insamt_sum - feeamt_sum
    lc = loancalc(request.user)
    p_list = lc.getmonthdue()
    lu = {}
    lu['due_category'] = p_list['d_days']
    lu['d_series'] = p_list['d_series']
    lu['d_drilldownSeries'] = p_list['d_drilldownSeries']

    lu['d_pf_inner_series'] = p_list['d_pf_inner_series']
    lu['d_pf_outer_series'] = p_list['d_pf_outer_series']

    lu['today_due_list'] = p_list['today_due_list']
    lu['record_number'] = p_list['today_due_list'].count()
    lu['insamt_sum'] = p_list['insamt_sum']
    lu['ownamt_sum'] = p_list['ownamt_sum']
    lu['feeamt_sum'] = p_list['feeamt_sum']
    lu['ownamt_sum'] = p_list['ownamt_sum']
    lu['amount_sum'] = p_list['amount_sum']
    del lc
    return render_to_response('welcome.html', lu, RequestContext(request))

def wxfocus(request):
    return render_to_response('wxfocus.html',RequestContext(request))


def logout(request):
    auth.logout(request)
    return render_to_response("login.html")
    
def login(request):
    redirect_to = request.REQUEST.get('next')
    if not redirect_to:
        redirect_to = '/welcome'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(redirect_to)
        else:
            # Show an error page
            return render_to_response("login.html",({'errormsg':u'用户名或密码错误'}), RequestContext(request))
    else:
        return render_to_response("login.html",{'next': redirect_to,}, RequestContext(request))