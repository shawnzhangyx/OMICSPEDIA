from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name = 'wiki-index'),
    url(r'^create/$', views.WikiNew.as_view(), name = 'wiki-new'),
    url(r'^(?P<pk>\d+)/$', views.WikiDetails.as_view(), name='wiki-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.WikiEdit.as_view(), name='wiki-edit'),
    url(r'^(?P<pk>\d+)/history/$', views.WikiHistory.as_view(), name='wiki-history'),
    url(r'^(?P<pk>\d+)/diff/$', views.WikiDiff.as_view(), name='wiki-diff'),
    )
