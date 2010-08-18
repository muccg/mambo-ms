from django.conf.urls.defaults import *
from django.contrib import admin
from mamboms.mambomsapp import admin as mamboms_admin
from mamboms import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^(.*)static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_SERVER_PATH} ),
    (r'^(.*)site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_SERVER_PATH}),
    (r'^$', 'mamboms.mambomsapp.views.frontend'),
    (r'^mamboms/', include('mamboms.mambomsapp.urls')),
    (r'^user/', include('mamboms.mambomsuser.urls')),
    (r'^reference/', include('mamboms.mambomsapp.urls')),
    (r'^msadmin/(.*)', admin.site.root),
    (r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'admin/login.html', 'SSL':True }),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)
