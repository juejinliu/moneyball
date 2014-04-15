# -*- coding: utf-8 -*- 
from django.conf.urls import *

urlpatterns = patterns('moneyball.wx.views',
    url(r'^$', 'weixin', name='weixin'),
#     url(r'^bindwxid/\?action=.+\?wxid=.+/$', 'bindwxid', name='bind_weixin_id'),
    url(r'^bindwxid/', 'bindwxid', name='bind_weixin_id'),
)
