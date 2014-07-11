from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.index_view, name = 'tag-index'),
    url(r'^(?P<pk>\d+)/$', views.TagDetails.as_view(), name='tag-detail'),
    url(r'^(?P<pk>\d+)/delete$', views.TagDelete.as_view(), name='tag-delete'),
    )
