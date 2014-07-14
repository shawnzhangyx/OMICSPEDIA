from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name = 'tool-index'),
    url(r'^create/$', views.ToolNew.as_view(), name = 'tool-new'),
    url(r'^(?P<pk>\d+)/$', views.ToolDetails.as_view(), name='tool-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.ToolEdit.as_view(), name='tool-edit'),
    )
