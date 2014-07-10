from django.conf.urls import patterns, url

from . import views 

urlpatterns = patterns('', 
    url(r'^$', views.IndexView.as_view(), name = 'post-index'),
    url(r'^create/$', views.PostNew.as_view(), name = 'post-new'),
    url(r'^(?P<pk>\d+)/$', views.PostDetails.as_view(), name='post-detail'),
    #url(r'^(?P<pk>\d+)/edit/$', views.PostEdit.as_view(), name='post-edit'),
    #url(r'^(?P<pk>\d+)/answer$',views.PostNewAnswer.as_view(), name ='post-new-answer'),
    )
