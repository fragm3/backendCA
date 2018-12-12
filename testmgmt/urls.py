from django.conf.urls import include, url


urlpatterns = [

    # Fetch All Questions
     url(r'crud_testfolders/$', 'testmgmt.views.crud_testfolders'),
]
