from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name = 'software-index'),
    url(r'^pre-create/$', views.software_precreate_view, name = 'software-precreate'),
    url(r'^create/$', views.SoftwareNew.as_view(), name = 'software-new'),
    url(r'^(?P<name>[^/]+)/$', views.SoftwareDetailView.as_view(), name='software-detail'),
    url(r'^(?P<name>[^/]+)/edit/$', views.SoftwareEditView.as_view(), name='software-edit'),
    )
