from django.conf.urls import patterns, url 

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ModeratePortal.as_view(), name='moderate-portal'),
    ### moderate wiki
    url(r'^wiki-list/$', views.ModerateWikiList.as_view(), name='wiki-list'),
    url(r'^wiki/(?P<title>[^/]+)/$', views.ModerateWiki.as_view(), name='wiki'),
    url(r'^wiki/change-wiki-status/(?P<title>[^/]+)/$', views.ChangeWikiStatus.as_view(), name='change-wiki-status'),
    url(r'^wiki/change-comment-status/(?P<pk>[^/]+)/$', views.ChangeWikiCommentStatus.as_view(), name='change-wiki-comment-status'),
    ### moderate tags
    url(r'^tag-list/$', views.ModerateTagList.as_view(), name='tag-list'),
    url(r'^tags/(?P<name>[^/]+)/$', views.ModerateTag.as_view(), name='tag'),
    url(r'^tags/change-tag-status/(?P<name>[^/]+)/$', views.ChangeTagStatus.as_view(), name='change-tag-status'),
    
)