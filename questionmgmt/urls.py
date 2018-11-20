from django.conf.urls import include, url


urlpatterns = [
    # Fetch All Questions
    url(r'fetch_all_questions/$', 'questionmgmt.views.fetch_all_questions'),
]
