# -*- coding: utf-8 -*- 
from django.conf.urls import *

urlpatterns = patterns('moneyball.wx.views',
    url(r'^$', 'weixin', name='weixin'),
    url(r'^(?P<wxid>\d+)/$', 'weixin', name='add_update_one_loan'),
)
