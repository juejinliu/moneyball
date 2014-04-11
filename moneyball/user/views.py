# -*- coding: utf-8 -*- 
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import RequestContext
from moneyball.user.forms import RegisterForm,ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm

# Create your views here.
def index(request):
    return render_to_response('index.html')

def registe(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, (u'Thank you for registering, %s. You are now logged in.' % user.username))
                return HttpResponseRedirect('/welcome')
            messages.add_message(request, messages.SUCCESS, (u'Thank you for registering, %s. You may now proceed to log in.' % user.username))
            return render_to_response("login.html", context_instance=RequestContext(request))
        
        else:
            # Show an error page
            return render_to_response("registe.html", { 'form': form }, context_instance=RequestContext(request))
    else:
        form = RegisterForm()
        return render_to_response("registe.html", { 'form': form }, context_instance=RequestContext(request))

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            return render_to_response("success.html",({'infomsg':u'修改成功'}), RequestContext(request))
        else:
            # Show an error page
            return render_to_response("profile.html", { 'form': form }, context_instance=RequestContext(request))
    else:
        form = ProfileForm(request.user)
        return render_to_response("profile.html", { 'form': form }, context_instance=RequestContext(request))
    
def passwordset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            return render_to_response("success.html",({'infomsg':u'修改成功'}), RequestContext(request))
        else:
            # Show an error page
            return render_to_response("passwordset.html", { 'form': form }, context_instance=RequestContext(request))
    else:
        form = PasswordChangeForm(request.user)
        return render_to_response("passwordset.html", { 'form': form }, context_instance=RequestContext(request))

def iforgot(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            return render_to_response("login.html",({'infomsg':u'已发送重置邮件到您信箱'}), RequestContext(request))
        else:
            # Show an error page
            return render_to_response("login.html", { 'form': form }, context_instance=RequestContext(request))
