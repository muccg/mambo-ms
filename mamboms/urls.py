from django.conf.urls.defaults import *
from django.contrib import admin
from mamboms.mambomsapp import admin as mamboms_admin
from mamboms import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^$', 'mamboms.mambomsapp.views.frontend'),
    (r'^$', 'mamboms.mambomsapp.views.site_frontend'),
    (r'^mamboms/', include('mamboms.mambomsapp.urls')),
    (r'^user/', include('mamboms.mambomsuser.urls')),
    (r'^reference/', include('mamboms.mambomsapp.urls')),
    (r'^msadmin/(.*)', include(admin.site.urls)),
    (r'^import/fileupload$', 'util_scripts.dataimporter.datafile_upload'),
    (r'^import/definefields$', 'util_scripts.dataimporter.define_fields'),
    (r'^import/confirmimport$', 'util_scripts.dataimporter.confirm_import'),
    (r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'admin/login.html', 'SSL':True }),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True} ),
    )
