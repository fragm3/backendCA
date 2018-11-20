from django.conf.urls import include, url


urlpatterns = [

    # Fetch All Questions
    url(r'fetch_all_users/$', 'overall.views.fetch_all_alfa'),
]
