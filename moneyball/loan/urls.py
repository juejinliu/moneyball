# -*- coding: utf-8 -*- 
from django.conf.urls import *

urlpatterns = patterns('moneyball.loan.views',
    url(r'^$', 'loaninfo'),
    url(r'^add/$', 'loaninfo'),
    url(r'^loansummary/$', 'loansummary'),
    url(r'^platform/$', 'platforminfo'),
    url(r'^loanlist/$', 'index'),
    url(r'^loandetaillist/$', 'index'),
    
    
)
