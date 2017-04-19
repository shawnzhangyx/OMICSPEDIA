from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.TagList.as_view(), name = 'tag-index'),
    url(r'^suggest_tag/$', views.suggest_tags, name='tag-suggest'),
    url(r'^create_tag/(?P<parent_name>[^/]*)/?$', views.TagCreate.as_view(), name='tag-create'),
    url(r'^(?P<name>[^/]+)/$', views.TagDetails.as_view(), name='tag-detail'),
    url(r'^(?P<name>[^/]+)/(?P<user>[^/]+)/$', views.TagUserContributionView.as_view(), name='tag-user'),
    url(r'^(?P<name>[^/]+)/edit$', views.TagEdit.as_view(), name='tag-edit'),
    url(r'^(?P<name>[^/]+)/delete$', views.TagDelete.as_view(), name='tag-delete'),
    )
