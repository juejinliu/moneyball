from django.conf.urls import patterns, include, url

urlpatterns = patterns('moneyball.user.views',
    url(r'^$', 'index'),
    url(r'^registe/$', 'registe'),
)
