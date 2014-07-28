from django.conf.urls import patterns, url
from . import views
urlpatterns = patterns('', 
url(r'^login/',views.Login.as_view(), name = "login"),
url(r'^logout/', views.Logout.as_view(), name="logout"),
url(r'^user/(?P<pk>\d+)/', views.ProfileView.as_view(), name="profile-view"),
url(r'^register/', views.RegisterView.as_view(), name="register"),
)
