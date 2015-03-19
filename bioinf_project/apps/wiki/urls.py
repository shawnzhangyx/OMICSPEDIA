from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    ## moderate views
    url(r'^moderatelist/$', views.WikiModerateList.as_view(), name="wiki-moderate-list"),
    url(r'^(?P<title>[^/]+)/moderate/$', views.WikiModerate.as_view(), name="wiki-moderate"),
    
    url(r'^$', views.IndexView.as_view(), name = 'wiki-index'),
    url(r'^list/$', views.WikiListView.as_view(), name = 'wiki-list'),
    url(r'^update/$', views.PageRevisionListView.as_view(), name = 'wiki-revision-list'),
    url(r'^article/create/$', views.WikiNew.as_view(), name = 'wiki-new'),
    url(r'^(?P<title>[^/]+)/$', views.WikiDetails.as_view(), name='wiki-detail'),
    url(r'^(?P<title>[^/]+)/edit/$', views.WikiEdit.as_view(), name='wiki-edit'),
    url(r'^(?P<title>[^/]+)/edit-section/$', views.wiki_section_edit, name='wiki-section-edit'),
    url(r'^(?P<title>[^/]+)/comment/$', views.WikiCommentView.as_view(), name='wiki-comment'),
    url(r'^(?P<title>[^/]+)/comment/add$', views.WikiCommentAdd.as_view(), name='wiki-comment-add'),
    url(r'^[^/]+/comment/(?P<pk>\d+)/edit$', views.WikiCommentEdit.as_view(), name='wiki-comment-edit'),
    url(r'^(?P<title>[^/]+)/history/$', views.WikiHistory.as_view(), name='wiki-history'),
    url(r'^(?P<title>[^/]+)/user-contribtion/$', views.UserPageView.as_view(), name='wiki-contributors'),
    url(r'^(?P<pk>\d+)/diff/$', views.WikiDiff.as_view(), name='wiki-diff'),

    ## ajax for wikilinks
    url(r'^ajax/wikilinks/$', views.wikilinks, name='wikilinks'),
    )
