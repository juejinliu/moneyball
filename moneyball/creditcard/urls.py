from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth import *

urlpatterns = patterns('moneyball.user.views',
    url(r'^$', 'index'),

)
