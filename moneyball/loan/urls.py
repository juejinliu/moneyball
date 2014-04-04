# -*- coding: utf-8 -*- 
from django.conf.urls import *

urlpatterns = patterns('moneyball.loan.views',
    url(r'^$', 'loaninfo'),
    url(r'^add/$', 'loaninfo'),
    url(r'^loansummary/$', 'loansummary'),
    url(r'^platform/$', 'platforminfo'),
    url(r'^loanlist/$', 'loanlist'),
    url(r'^loandetaillist/$', 'loandetaillist'),
    url(r'^loan_detail_return.*', 'loan_detail_return'),
    url(r'^loan_detail_no_return.*', 'loan_detail_no_return'),
    url(r'^loan_detail_bad.*', 'loan_detail_bad'),
)
