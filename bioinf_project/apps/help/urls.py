from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<help_page>.+)$', views.page_view, name = 'help-page'),
        )
