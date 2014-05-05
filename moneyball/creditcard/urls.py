from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth import *

urlpatterns = patterns('moneyball.creditcard.views',
    url(r'^$', 'index'),
    url(r'^creditcard/$', 'creditcardinfo', name='action_all_creditcard'),
    url(r'^creditcard/(?P<ccid>\d+)/$', 'creditcardinfo', name='action_one_creditcard'),
    url(r'^creditcard/(?P<ccid>\d+)/(?P<status>\d+)/$', 'creditcardinfo', name='hide_creditcard'),
    url(r'^billinfo/$', 'billinfo', name='action_all_billinfo'),
    url(r'^billinfo/(?P<biid>\d+)/$', 'billinfo', name='action_one_billinfo'),
    url(r'^billinfo/(?P<biid>\d+)/(?P<status>\d+)/$', 'billinfo', name='update_billinfo'),
    url(r'^billpay/$', 'billpay', name='action_all_billpay'),
    url(r'^billpay/(?P<bpid>\d+)/$', 'billpay', name='action_one_billpay'),
)
