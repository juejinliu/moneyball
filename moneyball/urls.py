from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'moneyball.common.views.index'),
    (r'^login/$', 'moneyball.common.views.login'),
    (r'^logout/$', 'moneyball.common.views.logout'),
    (r'^welcome/$', 'moneyball.common.views.welcome'),
    (r'^wxfocus/$', 'moneyball.common.views.wxfocus'),
    (r'^user/', include('moneyball.user.urls')),
    (r'^loan/', include('moneyball.loan.urls')),
    #(r'^accounts/', include('moneyball.accounts.urls')),
    #(r'^creditcard/', include('moneyball.creditcard.urls')),
    #(r'^moneyflow/', include('moneyball.moneyflow.urls')),
    #(r'^reports/', include('moneyball.reports.urls')),
    # Examples:
    # url(r'^$', 'moneyball.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
