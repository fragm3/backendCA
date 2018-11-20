from django.conf.urls import include, url


urlpatterns = [

    # Fetch All Questions
    url(r'fetch_all_users/$', 'usermgmt.views.fetch_all_users'),
]
