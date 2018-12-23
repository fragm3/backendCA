from django.conf.urls import include, url


urlpatterns = [
    # Fetch All Questions
    # url(r'crud_questions/$', 'questionmgmt.views.crud_questions'),
    url(r'crud_topics/$', 'questionmgmt.views.crud_topics'),
    url(r'crud_folders/$', 'questionmgmt.views.crud_folders'),
    url(r'crud_passages/$', 'questionmgmt.views.crud_passages'),
    url(r'crud_questions/$', 'questionmgmt.views.crud_questions'),
    url(r'check_api/$', 'questionmgmt.views.check_api'),
    url(r'check_answer_api/$', 'questionmgmt.views.check_answer_api'),
    
]
