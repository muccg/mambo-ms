from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'graph/(?P<compound_id>\d+)/$', 'mamboms.mambomsapp.views.graph'),
#    (r'graph/image/(?P<compound_id>\d+)/$', 'mamboms.mambomsapp.views.graph_image'),
    (r'graph/image/(?P<compound_id>\d+)/(?P<datastart>\d+)/(?P<dataend>\d+)/$', 'mamboms.mambomsapp.views.graph_image'),
#    (r'graph/image/(?P<compound_id>\d+)/xrange/(?P<xstart>\d+)/(?P<xend>\d+)/$', 'mamboms.mambomsapp.views.graph_image_xrange'),
#    (r'graph/image/calculate/(?P<compound_id>\d+)/(?P<curstartx>\d+)/(?P<curendx>\d+)/(?P<startx>\d+)/(?P<endx>\d+)/$', 'mamboms.mambomsapp.views.graph_image_calculate'),
    (r'graph/imageaction/$', 'mamboms.mambomsapp.views.graph_image_action'),
    (r'search/dotsearchjson/(?P<id>\d+)/(?P<num>\d+)/(?P<pagenum>\d+)/$', 'mamboms.mambomsapp.views.dotsearchJSON'),
    (r'search/dot/(?P<id>\d+)/(?P<num>\d+)/$', 'mamboms.mambomsapp.views.dotsearchMain'),
)
