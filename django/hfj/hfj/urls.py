from django.conf.urls import patterns, url
from base import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^bannerocity/(?:(?P<lesson>\d+)/)?$',
        views.bannerocity, name='bannerocity'),
    url(r'^bsi/(?:(?P<lesson>\d+)/)?$', views.bsi, name='bsi'),
    url(r'^donuts/(?:(?P<lesson>\d+)/)?$', views.donuts, name='donuts'),
    url(r'^youcube/$', views.youcube, name='youcube'),
    url(r'^youcube/add/$', views.youcube_add, name='youcube_add'),
)
