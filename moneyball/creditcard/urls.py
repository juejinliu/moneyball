from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth import *

urlpatterns = patterns('moneyball.creditcard.views',
    url(r'^$', 'index'),
    url(r'^creditcard/$', 'creditcardinfo', name='action_all_creditcard'),
    url(r'^creditcard/(?P<ccid>\d+)/$', 'creditcardinfo', name='action_one_creditcard'),
    url(r'^creditcard/(?P<ccid>\d+)/(?P<status>\d+)/$', 'creditcardinfo', name='hide_creditcard'),

)
