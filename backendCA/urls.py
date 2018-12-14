from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backendCA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^question/', include('questionmgmt.urls')),
    url(r'^test/', include('testmgmt.urls')),
    url(r'^user/', include('usermgmt.urls')),
    url(r'^overall/', include('overall.urls')),

)



