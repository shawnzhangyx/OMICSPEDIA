from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name = 'meta-index'),
    url(r'^create/$', views.ReportNew.as_view(), name = 'report-new'),
    url(r'^(?P<pk>\d+)/$', views.ReportDetails.as_view(), name='report-detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.ReportEdit.as_view(), name='report-edit'),
#    url(r'^(?P<mainpost_id>\d+)/reply-new/$', views.ReplyPostNew.as_view(), name='replypost-new'),
#    url(r'^(?P<pk>\d+)/reply-edit/$', views.ReplyPostEdit.as_view(), name='replypost-edit'),
#    url(r'^(?P<pk>\d+)/reply-delete/$', views.ReplyPostDelete.as_view(), name='replypost-delete'),
    )
