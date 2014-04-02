# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from moneyball.loan.models import Loandetail
# Create your views here.
def index(request):
    return render_to_response('index.html')

@login_required
def welcome(request):
    today_due_list = Loandetail.objects.all()
    return render_to_response('welcome.html', {"today_due_list": today_due_list}, RequestContext(request))

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