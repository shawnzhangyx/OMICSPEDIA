from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bioinf_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wiki/', include('wiki.urls', namespace = "wiki")),
    url(r'^tags/', include('tags.urls', namespace = "tags")),
    url(r'^posts/', include('posts.urls', namespace = "posts")),
#    url(r'^tool/', include('tool_wiki.urls', namespace = "tool")),
#    url(r'^code_snippet/', include('code_snippet_repos.urls', namespace = "wiki")),
)
