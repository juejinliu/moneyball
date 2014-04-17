# -*- coding: utf-8 -*- 
from django.conf.urls import *

urlpatterns = patterns('moneyball.loan.views',
    url(r'^$', 'loaninfo', name='action_all_loan'),
    url(r'^(?P<lnid>\d+)/$', 'loaninfo', name='add_update_one_loan'),
    url(r'^loanquery/(?P<lnid>\d+)/$', 'loaninfo', name='query_one_loan'),
    url(r'^loandelete/(?P<lnid>\d+)/$', 'loandelete', name='delete_one_loan'),
    url(r'^loansummary/$', 'loansummary',name='loan_summary'),
    url(r'^platform/$', 'platforminfo', name='action_all_platform'),
    url(r'^getplatformfee/$', 'getplatformfee', name='get_platform_fee'),
#     url(r'^getpfsum/$', 'getpfduesum', name='get_platform_duesum'),
    url(r'^platform/(?P<pfid>\d+)/$', 'platforminfo', name='action_one_platform'),
    url(r'^platform/(?P<pfid>\d+)/(?P<status>\d+)/$', 'platforminfo', name='hide_platform'),
    url(r'^loanlist/$', 'loanlist'),
    url(r'^loandetaillist/$', 'loandetaillist'),
#     url(r'^update_loandtl_loanid/$', 'update_loandtl_loanid'),  #修改导入数据用，正常环境不启用
    url(r'^loan_detail_return.*', 'loan_detail_return'),
    url(r'^loan_detail_no_return.*', 'loan_detail_no_return'),
    url(r'^loan_detail_bad.*', 'loan_detail_bad'),
)
