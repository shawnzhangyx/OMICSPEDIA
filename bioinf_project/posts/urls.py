from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name = 'post-index'),
    url(r'^create/$', views.MainPostNew.as_view(), name = 'post-new'),
    url(r'^(?P<pk>\d+)/$', views.PostDetails.as_view(), name='post-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.MainPostEdit.as_view(), name='mainpost-edit'),
    url(r'^(?P<mainpost_id>\d+)/reply-new/$', views.ReplyPostNew.as_view(), name='replypost-new'),
    url(r'^(?P<pk>\d+)/reply-edit/$', views.ReplyPostEdit.as_view(), name='replypost-edit'),
    url(r'^(?P<pk>\d+)/reply-delete/$', views.ReplyPostDelete.as_view(), name='replypost-delete'),

    )
