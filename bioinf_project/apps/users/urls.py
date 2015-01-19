from django.conf.urls import patterns, url
from . import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done

urlpatterns = patterns('', 
url(r'^login/$',views.Login.as_view(), name = "login"),
url(r'^logout/$', views.Logout.as_view(), name="logout"),
url(r'^user/(?P<pk>\d+)/$', views.ProfileView.as_view(), name="profile-view"),
url(r'^user/(?P<pk>\d+)/edit$', views.ProfileEdit.as_view(), name="profile-edit"),
url(r'^user/(?P<pk>\d+)/following/$', views.FollowingListView.as_view(), name="following"),
url(r'^user/(?P<pk>\d+)/followers/$', views.FollowerListView.as_view(), name="followers"),
url(r'^user/(?P<pk>\d+)/notifications/(?P<type>[^/]+)/$', views.NotificationListView.as_view(), name="notifications"),
url(r'^user/(?P<pk>\d+)/change-follower/$', views.FollowerEditView.as_view(), name='change-follow'),
url(r'^users/$', views.UserListView.as_view(), name="user-list"),
url(r'^register/$', views.RegisterView.as_view(), name="register"),
url(r'^email-verification/(?P<sent>(sent)?)/?$', views.email_verification_form, name="email-verification-form"),
url(r'^email-verification-complete/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.email_verification_complete, name="email-verification-complete"),
url(r'^password/change/$', password_change, {'template_name':'users/password_change_form.html','post_change_redirect':'/accounts/password/change_done/'}, name="password-change"),
url(r'^password/change_done/$', password_change_done, {'template_name':'users/password_change_done.html'}, name="password_change_done"),
url(r'^password/reset/$', password_reset, {'post_reset_redirect':'/accounts/password/reset/done/', 'template_name':'users/password_reset_form.html', 'email_template_name':'users/password_reset_email.html'}, name="password-reset"),
url(r'^password/reset/done/$', password_reset_done, {'template_name': 'users/password_reset_done.html'}),
url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name':'users/password_reset_confirm.html', 'post_reset_redirect':'/accounts/password/reset/complete/'}, name="password-reset-confirm"),
url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'users/password_reset_complete.html'}),
url(r'^ajax/read-notification/$', views.read_notification, name="read-notification"),

)
