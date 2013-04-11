from django.contrib import admin
from mamboms.mambomsapp import models

class CompoundAdmin(admin.ModelAdmin):
    list_display = ('truncated_name', 'link_to_graph', 'cas_regno', 'molecular_formula')
    search_fields = ['name', 'cas_regno', 'molecular_formula']
    list_filter = ('dataset',)

class RestrictedModelAdmin(admin.ModelAdmin):
    '''ModelAdmin subclass for classes that have to restrict the editable data'''

    def is_admin(self, user):
        return (user.is_superuser
            or (user.get_profile() and user.get_profile().get_details().get('isAdmin')))

    def queryset(self, request):
        queryset = super(RestrictedModelAdmin, self).queryset(request)
        if self.is_admin(request.user):
            return queryset 
        return self.filter_user_queryset(queryset, request)

    def get_form(self, request, obj=None):
        form = super(RestrictedModelAdmin, self).get_form(request, obj)
        if self.is_admin(request.user):
            return form
        return self.filter_user_form(form, request)

    def get_changelist_form(self, request, **kwargs):
        form = super(RestrictedModelAdmin, self).get_changelist_form(request, **kwargs)
        if self.is_admin(request.user):
            return form
        return self.filter_user_form(form, request)

    def get_changelist_formset(self, request, **kwargs):
        formset = super(RestrictedModelAdmin, self).get_changelist_formset(request, **kwargs)
        if self.is_admin(request.user):
            return formset
        formset.form = self.filter_user_form(formset.form, request)
        return formset

    def filter_user_form(self, form, request):
        return form

    def filter_user_queryset(self, queryset, request):
        return queryset

class RestrictedByNodeAdmin(RestrictedModelAdmin):
    def filter_user_form(self, form, request):
        user_node = request.user.get_profile().node
        form.base_fields['node'].queryset = models.Node.objects.filter(name = user_node)
        form.base_fields['node'].empty_label = None
        return form

    def filter_user_queryset(self, queryset, request):
        user_node = request.user.get_profile().node
        return queryset.filter(node__name = user_node)

class InstrumentAdmin(RestrictedByNodeAdmin):
    list_display = ('node', 'name')

class GCMethodAdmin(RestrictedByNodeAdmin):
    list_display = ('node', 'name')   

class LCMethodAdmin(RestrictedByNodeAdmin):
    list_display = ('node', 'name')   

class ColumnAdmin(RestrictedByNodeAdmin):
    list_display = ('node', 'name')   

admin.site.register(models.Compound, CompoundAdmin)
admin.site.register(models.Dataset)
admin.site.register(models.Node)
admin.site.register(models.ChromatographyType)
admin.site.register(models.MSGeometry)
admin.site.register(models.IonizationMode)
admin.site.register(models.Instrument, InstrumentAdmin)
admin.site.register(models.GCMethod, GCMethodAdmin)
admin.site.register(models.LCMethod, LCMethodAdmin)
admin.site.register(models.LCModification)
admin.site.register(models.Column, ColumnAdmin)
admin.site.register(models.BiologicalSystem)
admin.site.register(models.MassSpectraType)
admin.site.register(models.MetaboliteClass)
admin.site.register(models.PrecursorType)
admin.site.register(models.Spectrum)
