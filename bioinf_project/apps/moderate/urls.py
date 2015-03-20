from django.conf.urls import patterns, url 

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ModeratePortal.as_view(), name='moderate-portal'),
    url(r'^wiki-list/$', views.ModerateWikiList.as_view(), name='wiki-list'),
    url(r'^wiki/(?P<title>[^/]+)/$', views.ModerateWiki.as_view(), name='wiki'),
    url(r'^wiki/change-wiki-status/(?P<title>[^/]+)/$', views.ChangeWikiStatus.as_view(), name='change-wiki-status'),
    url(r'^wiki/change-comment-status/(?P<pk>[^/]+)/$', views.ChangeWikiCommentStatus.as_view(), name='change-wiki-comment-status'),

)