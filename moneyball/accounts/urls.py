from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth import *

urlpatterns = patterns('moneyball.user.views',
    url(r'^$', 'index'),
    url(r'^registe/$', 'registe'),
    url(r'^profile/$', 'profile'),
    url(r'^passwordset/$', 'passwordset'),
    url(r'^iforgot/$', 'iforgot'),
)
urlpatterns += patterns('',
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', \
        'django.contrib.auth.views.password_reset_confirm', {
        'template_name': 'password_reset_confirm.html',
        'post_reset_redirect': '/',
        },name='password_reset_confirm',
     ),
    
)
