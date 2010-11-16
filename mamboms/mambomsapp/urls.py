from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Spectra Graph

    (r'graph/page', 'mamboms.mambomsapp.views.graph.page'),
    (r'graph/image/(?P<spectrum_id>\d+)/$', 'mamboms.mambomsapp.views.graph.start_image'),
    (r'graph/image/(?P<spectrum_id>\d+)/(?P<datastart>\d+)/(?P<dataend>\d+)/$', 'mamboms.mambomsapp.views.graph.image'),
    (r'graph/imagemap/(?P<spectrum_id>\d+)/$', 'mamboms.mambomsapp.views.graph.image_map'),
    (r'graph/imageaction/$', 'mamboms.mambomsapp.views.graph.image_action'),

    # Search

    (r'search/bykeyword/$', 'mamboms.mambomsapp.views.search.keyword_search'),
    (r'search/byspectra/$', 'mamboms.mambomsapp.views.search.spectra_search'),

    # TODO move the view functions from crazysearch to mamboms/views/something.py
    #These views are for creating and monitoring the Tokyo Hash. 
    (r'search/status/$', 'mamboms.mambomsapp.crazysearch.status'),
    (r'search/search/$', 'mamboms.mambomsapp.crazysearch.search'),
    (r'search/create/$', 'mamboms.mambomsapp.crazysearch.create_hash'),
    (r'search/build/$', 'mamboms.mambomsapp.crazysearch.build_hash'),

    # Reference data

    (r'gc_methods/bynode/$', 'mamboms.mambomsapp.views.reference_data.list_gcmethods', {'bynode' : "true"}),
    (r'gc_methods/$', 'mamboms.mambomsapp.views.reference_data.list_gcmethods'),
    (r'lc_methods/bynode/$', 'mamboms.mambomsapp.views.reference_data.list_lcmethods', {'bynode' : "false"}),
    (r'lc_methods/$', 'mamboms.mambomsapp.views.reference_data.list_lcmethods'),
    (r'columns/$', 'mamboms.mambomsapp.views.reference_data.list_columns'),
    (r'instruments/$', 'mamboms.mambomsapp.views.reference_data.list_instruments'),
    (r'biological_systems/$', 'mamboms.mambomsapp.views.reference_data.list_biological_systems'),
    (r'precursor_selections/$', 'mamboms.mambomsapp.views.reference_data.list_precursor_selections'),
    (r'precursor_types/$', 'mamboms.mambomsapp.views.reference_data.list_precursor_types'),
    (r'metabolite_classes/$', 'mamboms.mambomsapp.views.reference_data.list_metabolite_classes'),
    (r'ionized_species/$', 'mamboms.mambomsapp.views.reference_data.list_ionized_species'),
    (r'mass_spectra_types/$', 'mamboms.mambomsapp.views.reference_data.list_mass_spectra_types'),
    (r'derivitization_agents/$', 'mamboms.mambomsapp.views.reference_data.list_derivitization_agents'),
    (r'chromatography_types/$', 'mamboms.mambomsapp.views.reference_data.list_chromatography_types'),
    (r'msgeometry_types/$', 'mamboms.mambomsapp.views.reference_data.list_ms_geometry_types'),
    (r'ionization_modes/$', 'mamboms.mambomsapp.views.reference_data.list_ionization_modes'),
    (r'polarities/$', 'mamboms.mambomsapp.views.reference_data.list_polarities'),

    # GC and LC

    (r'lcmetabolite/save/$', 'mamboms.mambomsapp.views.metabolite.save_lc'),
    (r'metabolite/save/$', 'mamboms.mambomsapp.views.metabolite.save'),
    (r'metabolite/lc/load/$', 'mamboms.mambomsapp.views.metabolite.lcmetabolite_load'),
    (r'metabolite/gc/load/$', 'mamboms.mambomsapp.views.metabolite.gcmetabolite_load'),
    (r'metabolite/vet/$', 'mamboms.mambomsapp.views.metabolite.vet'),
    (r'metabolite/delete/$', 'mamboms.mambomsapp.views.metabolite.delete'),

    (r'frontend/$', 'mamboms.mambomsapp.views.frontend'),
    (r'files/(?P<path>.*)$', 'mamboms.mambomsapp.views.serve_file'),
)
