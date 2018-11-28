from django.conf.urls import include, url


urlpatterns = [
    # Fetch All Questions
    url(r'crud_users/$', 'usermgmt.views.crud_user'),
    url(r'login_user/$', 'usermgmt.views.login_view_staff'),
    url(r'send_password_reset_req/$', 'usermgmt.views.send_password_reset'),
    url(r'reset_pass_user/$', 'usermgmt.views.reset_pass_staff'),
    url(r'logout_user/$', 'usermgmt.views.logout_view_staff'),
]
