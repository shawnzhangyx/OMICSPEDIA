from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views
from utils.views import CommentNew, vote
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bioinf_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('users.urls', namespace = "users")),
    url(r'^wiki/', include('wiki.urls', namespace = "wiki")),
    url(r'^tags/', include('tags.urls', namespace = "tags")),
    url(r'^posts/', include('posts.urls', namespace = "posts")),
 #   url(r'^tools/', include('tool_wiki.urls', namespace = "tools")),
#    url(r'^code_snippet/', include('code_snippet_repos.urls', namespace = "wiki")),

    url(r'^(?P<comment_on>[^/]+)/(?P<pk>\d+)/comment-new/$', CommentNew.as_view(), name="comment-new"),
    url(r'^search/$', views.search, name='search'),
    url(r'^ajax/vote/$', vote, name='vote'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
