from django.conf.urls import *

urlpatterns = patterns('moneyball.loan.views',
    url(r'^$', 'index', name='loan-index'),
    url(r'^index/$', 'index', name='loan-index'),
)
