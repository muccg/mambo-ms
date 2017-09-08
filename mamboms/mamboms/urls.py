from django.conf.urls import patterns, url, include
from django.contrib import admin
from mamboms.mambomsapp import admin as mamboms_admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^$', 'mamboms.mambomsapp.views.frontend'),
    (r'^$', 'mamboms.mambomsapp.views.site_frontend'),
    (r'^mamboms/', include('mamboms.mambomsapp.urls')),
    (r'^user/', include('mamboms.mambomsuser.urls')),
    (r'^reference/', include('mamboms.mambomsapp.urls')),
    (r'^msadmin/', include(admin.site.urls)),
    (r'^import/fileupload$', 'mamboms.util_scripts.dataimporter.datafile_upload'),
    (r'^import/definefields$', 'mamboms.util_scripts.dataimporter.define_fields'),
    (r'^import/confirmimport$', 'mamboms.util_scripts.dataimporter.confirm_import'),
    (r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'admin/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT} ),
    )
