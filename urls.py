from django.conf.urls.defaults import *
from django.contrib import admin
from mamboms.mambomsapp import admin as mamboms_admin
from mamboms import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^mamboms/', include('mamboms.mambomsapp.urls')),
    (r'^admin/(.*)', admin.site.root, {'SSL':False}),
    (r'^(.*)site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_SERVER_PATH}),
    # Uncomment the next line to enable the admin:
    (r'^(.*)', admin.site.root, {'SSL':True}),


)
