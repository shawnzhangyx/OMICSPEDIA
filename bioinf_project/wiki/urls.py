from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name = 'wiki-index'),
    url(r'^create/$', views.WikiNew.as_view(), name = 'wiki-new'),
    url(r'^(?P<title>[^/]+)/$', views.WikiDetails.as_view(), name='wiki-detail'),
    url(r'^(?P<title>[^/]+)/edit/$', views.WikiEdit.as_view(), name='wiki-edit'),
    url(r'^(?P<title>[^/]+)/edit-section/$', views.wiki_section_edit, name='wiki-section-edit'),
    url(r'^(?P<title>[^/]+)/comment/$', views.WikiCommentView.as_view(), name='wiki-comment'),
    url(r'^(?P<title>[^/]+)/comment/add$', views.WikiCommentAdd.as_view(), name='wiki-comment-add'),
    url(r'^[^/]+/comment/(?P<pk>\d+)/edit$', views.WikiCommentEdit.as_view(), name='wiki-comment-edit'),
    url(r'^(?P<title>[^/]+)/history/$', views.WikiHistory.as_view(), name='wiki-history'),
    url(r'^(?P<pk>\d+)/diff/$', views.WikiDiff.as_view(), name='wiki-diff'),
    )
