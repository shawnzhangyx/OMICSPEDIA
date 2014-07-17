from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.TagList.as_view(), name = 'tag-index'),
    url(r'^create_tag/$', views.TagCreate.as_view(), name='tag-create'),
    url(r'^(?P<pk>\d+)/$', views.TagDetails.as_view(), name='tag-detail'),
    url(r'^(?P<pk>\d+)/delete$', views.TagDelete.as_view(), name='tag-delete'),
    )
