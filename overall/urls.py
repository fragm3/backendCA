from django.conf.urls import include, url


urlpatterns = [

    url(r'upload_file/$', 'overall.views.upload_file'),
]
