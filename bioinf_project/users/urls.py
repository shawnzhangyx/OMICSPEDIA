from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', 
url(r'^login/',views.Login.as_view(), name = "login"),
)
