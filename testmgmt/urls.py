from django.conf.urls import include, url


urlpatterns = [

    # Fetch All Questions
    url(r'fetch_all_tests/$', 'testmgmt.views.fetch_all_tests'),
]
