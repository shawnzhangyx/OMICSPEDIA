from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^tagged/(?P<tag>[^/]+)/$', views.IndexView.as_view(), name = 'software-index'),
    url(r'^list$', views.SoftwareListView.as_view(), name = 'software-list'),
    url(r'^create/$', views.SoftwareNew.as_view(), name = 'software-new'),
    url(r'^(?P<name>[^/]+)/$', views.SoftwareDetailView.as_view(), name='software-detail'),
    url(r'^(?P<name>[^/]+)/edit/$', views.SoftwareEditView.as_view(), name='software-edit'),
    )
