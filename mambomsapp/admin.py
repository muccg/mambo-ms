from django.contrib import admin
from mamboms.mambomsapp.models import Compound, Point, Dataset

class PointInline(admin.TabularInline):
    model = Point

class CompoundAdmin(admin.ModelAdmin):
    list_display = ('truncated_name', 'link_to_graph', 'link_to_dotsearch', 'cas_regno', 'molecular_formula')
    inlines = (PointInline,)
    search_fields = ['name', 'cas_regno', 'molecular_formula']
    list_filter = ('dataset',)
    


admin.site.register(Compound, CompoundAdmin)
admin.site.register(Dataset)

