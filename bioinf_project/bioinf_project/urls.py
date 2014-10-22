from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views
from utils.views import CommentNew, vote, rate, preview_markdown
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bioinf_project.views.home', name='home'),
    # OmicsPedia Home page
    url(r'^$', views.IndexView.as_view(), name="index"),
    # Admin site
    url(r'^admin/', include(admin.site.urls)),
    # Omics Portal
    url(r'^portal/(?P<name>[^/]*)/?', views.PortalView.as_view(), name="portal"),
    # app specific urls 
    url(r'^accounts/', include('users.urls', namespace = "users")),
    url(r'^wiki/', include('wiki.urls', namespace = "wiki")),
    url(r'^tags/', include('tags.urls', namespace = "tags")),
    url(r'^posts/', include('posts.urls', namespace = "posts")),
    url(r'^software/', include('software.urls', namespace = "software")),
	url(r'^meta/', include('meta.urls', namespace = "meta")),
    url(r'^help/', include('help.urls', namespace="help")),
#    url(r'^code_snippet/', include('code_snippet_repos.urls', namespace = "wiki")),

    # util urls and ajax links
    url(r'^(?P<comment_on>[^/]+)/(?P<pk>\d+)/comment-new/$', CommentNew.as_view(), name="comment-new"),
    url(r'^search/$', views.search, name='search'),
    url(r'^ajax/omics-tag-description/', views.portal_tag, name="portal-omics-tag"),
    url(r'^ajax/vote/$', vote, name='vote'),
    url(r'^ajax/rate/$', rate, name='rate'),
    url(r'^ajax/preview-markdown/$', preview_markdown, name="preview-markdown"),
    )


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
