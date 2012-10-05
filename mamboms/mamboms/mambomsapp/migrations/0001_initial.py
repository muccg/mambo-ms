# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dataset'
        db.create_table('mambomsapp_dataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mambomsapp', ['Dataset'])

        # Adding model 'Compound'
        db.create_table('mambomsapp_compound', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Dataset'])),
            ('compound_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('cas_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cas_regno', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('molecular_formula', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('molecular_weight', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=18, decimal_places=10)),
        ))
        db.send_create_signal('mambomsapp', ['Compound'])

        # Adding model 'Node'
        db.create_table('mambomsapp_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['Node'])

        # Adding model 'ChromatographyType'
        db.create_table('mambomsapp_chromatographytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['ChromatographyType'])

        # Adding model 'MSGeometry'
        db.create_table('mambomsapp_msgeometry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['MSGeometry'])

        # Adding model 'IonizationMode'
        db.create_table('mambomsapp_ionizationmode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['IonizationMode'])

        # Adding model 'Instrument'
        db.create_table('mambomsapp_instrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['Instrument'])

        # Adding model 'GCMethod'
        db.create_table('mambomsapp_gcmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chromatography_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.ChromatographyType'])),
            ('ms_geometry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.MSGeometry'])),
            ('ionization_mode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.IonizationMode'])),
            ('polarity', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('derivitization_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mass_range_acquired', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('instrument_method', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True)),
            ('method_summary', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True)),
            ('mass_exp_deriv_adducts', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['GCMethod'])

        # Adding model 'LCMethod'
        db.create_table('mambomsapp_lcmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chromatography_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.ChromatographyType'])),
            ('ms_geometry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.MSGeometry'])),
            ('ionization_mode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.IonizationMode'])),
            ('polarity', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('derivitization_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mass_range_acquired', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('instrument_method', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True)),
            ('method_summary', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True)),
            ('mz_exp_deriv_adducts', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('flow_rate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('solvent_composition_a', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('solvent_composition_b', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('solvent_composition_c', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('solvent_composition_d', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['LCMethod'])

        # Adding model 'LCModification'
        db.create_table('mambomsapp_lcmodification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_of_compound', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mass', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('molecular_formula', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['LCModification'])

        # Adding model 'Column'
        db.create_table('mambomsapp_column', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('chromatography_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.ChromatographyType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('internal_diameter', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dimension', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('guard_column', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('product_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('particle_size', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['Column'])

        # Adding model 'BiologicalSystem'
        db.create_table('mambomsapp_biologicalsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kingdom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['BiologicalSystem'])

        # Adding model 'MARecordVet'
        db.create_table('mambomsapp_marecordvet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gc_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.GCMARecord'], null=True)),
            ('lc_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.LCMARecord'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('record_vetted_on', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mambomsapp', ['MARecordVet'])

        # Adding model 'MetaboliteClass'
        db.create_table('mambomsapp_metaboliteclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['MetaboliteClass'])

        # Adding model 'GCMARecord'
        db.create_table('mambomsapp_gcmarecord', (
            ('compound_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mambomsapp.Compound'], unique=True, primary_key=True)),
            ('known', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Instrument'])),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Column'])),
            ('sample_run_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gcmarecord_ran', to=orm['auth.User'])),
            ('record_uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gcmarecord_uploaded_records', to=orm['auth.User'])),
            ('record_uploaded_on', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('metabolite_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.MetaboliteClass'])),
            ('retention_time', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('retention_index', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('kegg_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('kegg_link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('extract_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('structure', self.gf('django.db.models.fields.files.FileField')(max_length=500, blank=True)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.GCMethod'])),
            ('quant_ion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('qualifying_ion_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('qualifying_ion_2', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('qualifying_ion_3', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
        ))
        db.send_create_signal('mambomsapp', ['GCMARecord'])

        # Adding M2M table for field biological_systems on 'GCMARecord'
        db.create_table('mambomsapp_gcmarecord_biological_systems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gcmarecord', models.ForeignKey(orm['mambomsapp.gcmarecord'], null=False)),
            ('biologicalsystem', models.ForeignKey(orm['mambomsapp.biologicalsystem'], null=False))
        ))
        db.create_unique('mambomsapp_gcmarecord_biological_systems', ['gcmarecord_id', 'biologicalsystem_id'])

        # Adding model 'LCMARecord'
        db.create_table('mambomsapp_lcmarecord', (
            ('compound_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mambomsapp.Compound'], unique=True, primary_key=True)),
            ('known', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Node'])),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Instrument'])),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Column'])),
            ('sample_run_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lcmarecord_ran', to=orm['auth.User'])),
            ('record_uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lcmarecord_uploaded_records', to=orm['auth.User'])),
            ('record_uploaded_on', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('metabolite_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.MetaboliteClass'])),
            ('retention_time', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('retention_index', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('kegg_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('kegg_link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('extract_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('structure', self.gf('django.db.models.fields.files.FileField')(max_length=500, blank=True)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.LCMethod'])),
            ('mono_isotopic_mass', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('mambomsapp', ['LCMARecord'])

        # Adding M2M table for field biological_systems on 'LCMARecord'
        db.create_table('mambomsapp_lcmarecord_biological_systems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lcmarecord', models.ForeignKey(orm['mambomsapp.lcmarecord'], null=False)),
            ('biologicalsystem', models.ForeignKey(orm['mambomsapp.biologicalsystem'], null=False))
        ))
        db.create_unique('mambomsapp_lcmarecord_biological_systems', ['lcmarecord_id', 'biologicalsystem_id'])

        # Adding model 'Synonym'
        db.create_table('mambomsapp_synonym', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ma_record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonyms', to=orm['mambomsapp.Compound'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['Synonym'])

        # Adding model 'PrecursorType'
        db.create_table('mambomsapp_precursortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('polarity', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('mambomsapp', ['PrecursorType'])

        # Adding model 'PrecursorSelection'
        db.create_table('mambomsapp_precursorselection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('mambomsapp', ['PrecursorSelection'])

        # Adding model 'MassSpectraType'
        db.create_table('mambomsapp_massspectratype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mambomsapp', ['MassSpectraType'])

        # Adding model 'Spectrum'
        db.create_table('mambomsapp_spectrum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compound', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Compound'])),
            ('raw_points', self.gf('django.db.models.fields.TextField')()),
            ('mass_spectra_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.MassSpectraType'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('precursor_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.PrecursorType'], null=True, blank=True)),
            ('precursor_selection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.PrecursorSelection'], null=True, blank=True)),
            ('collison_energy', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('precursor_mass', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=18, decimal_places=10)),
            ('precursor_ion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('product_ion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('fragment_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('mambomsapp', ['Spectrum'])

        # Adding M2M table for field ionized_species on 'Spectrum'
        db.create_table('mambomsapp_spectrum_ionized_species', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spectrum', models.ForeignKey(orm['mambomsapp.spectrum'], null=False)),
            ('lcmodification', models.ForeignKey(orm['mambomsapp.lcmodification'], null=False))
        ))
        db.create_unique('mambomsapp_spectrum_ionized_species', ['spectrum_id', 'lcmodification_id'])

        # Adding model 'HashMaintenance'
        db.create_table('mambomsapp_hashmaintenance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spectrum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mambomsapp.Spectrum'])),
            ('last_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mambomsapp', ['HashMaintenance'])


    def backwards(self, orm):
        
        # Deleting model 'Dataset'
        db.delete_table('mambomsapp_dataset')

        # Deleting model 'Compound'
        db.delete_table('mambomsapp_compound')

        # Deleting model 'Node'
        db.delete_table('mambomsapp_node')

        # Deleting model 'ChromatographyType'
        db.delete_table('mambomsapp_chromatographytype')

        # Deleting model 'MSGeometry'
        db.delete_table('mambomsapp_msgeometry')

        # Deleting model 'IonizationMode'
        db.delete_table('mambomsapp_ionizationmode')

        # Deleting model 'Instrument'
        db.delete_table('mambomsapp_instrument')

        # Deleting model 'GCMethod'
        db.delete_table('mambomsapp_gcmethod')

        # Deleting model 'LCMethod'
        db.delete_table('mambomsapp_lcmethod')

        # Deleting model 'LCModification'
        db.delete_table('mambomsapp_lcmodification')

        # Deleting model 'Column'
        db.delete_table('mambomsapp_column')

        # Deleting model 'BiologicalSystem'
        db.delete_table('mambomsapp_biologicalsystem')

        # Deleting model 'MARecordVet'
        db.delete_table('mambomsapp_marecordvet')

        # Deleting model 'MetaboliteClass'
        db.delete_table('mambomsapp_metaboliteclass')

        # Deleting model 'GCMARecord'
        db.delete_table('mambomsapp_gcmarecord')

        # Removing M2M table for field biological_systems on 'GCMARecord'
        db.delete_table('mambomsapp_gcmarecord_biological_systems')

        # Deleting model 'LCMARecord'
        db.delete_table('mambomsapp_lcmarecord')

        # Removing M2M table for field biological_systems on 'LCMARecord'
        db.delete_table('mambomsapp_lcmarecord_biological_systems')

        # Deleting model 'Synonym'
        db.delete_table('mambomsapp_synonym')

        # Deleting model 'PrecursorType'
        db.delete_table('mambomsapp_precursortype')

        # Deleting model 'PrecursorSelection'
        db.delete_table('mambomsapp_precursorselection')

        # Deleting model 'MassSpectraType'
        db.delete_table('mambomsapp_massspectratype')

        # Deleting model 'Spectrum'
        db.delete_table('mambomsapp_spectrum')

        # Removing M2M table for field ionized_species on 'Spectrum'
        db.delete_table('mambomsapp_spectrum_ionized_species')

        # Deleting model 'HashMaintenance'
        db.delete_table('mambomsapp_hashmaintenance')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mambomsapp.biologicalsystem': {
            'Meta': {'object_name': 'BiologicalSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.chromatographytype': {
            'Meta': {'object_name': 'ChromatographyType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mambomsapp.column': {
            'Meta': {'object_name': 'Column'},
            'chromatography_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.ChromatographyType']"}),
            'dimension': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'guard_column': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_diameter': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"}),
            'particle_size': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.compound': {
            'Meta': {'object_name': 'Compound'},
            'cas_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cas_regno': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'compound_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'molecular_formula': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'molecular_weight': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '18', 'decimal_places': '10'})
        },
        'mambomsapp.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.gcmarecord': {
            'Meta': {'object_name': 'GCMARecord'},
            'biological_systems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mambomsapp.BiologicalSystem']", 'symmetrical': 'False'}),
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Column']"}),
            'compound_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mambomsapp.Compound']", 'unique': 'True', 'primary_key': 'True'}),
            'extract_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Instrument']"}),
            'kegg_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'kegg_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'known': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metabolite_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.MetaboliteClass']"}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.GCMethod']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"}),
            'qualifying_ion_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'qualifying_ion_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'qualifying_ion_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'quant_ion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'record_uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gcmarecord_uploaded_records'", 'to': "orm['auth.User']"}),
            'record_uploaded_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'record_vets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'gcmarecord_vetted_records'", 'symmetrical': 'False', 'through': "orm['mambomsapp.MARecordVet']", 'to': "orm['auth.User']"}),
            'retention_index': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'retention_time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sample_run_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gcmarecord_ran'", 'to': "orm['auth.User']"}),
            'structure': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'})
        },
        'mambomsapp.gcmethod': {
            'Meta': {'object_name': 'GCMethod'},
            'chromatography_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.ChromatographyType']"}),
            'derivitization_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_method': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True'}),
            'ionization_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.IonizationMode']"}),
            'mass_exp_deriv_adducts': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mass_range_acquired': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method_summary': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True'}),
            'ms_geometry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.MSGeometry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"}),
            'polarity': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'mambomsapp.hashmaintenance': {
            'Meta': {'object_name': 'HashMaintenance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spectrum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Spectrum']"})
        },
        'mambomsapp.instrument': {
            'Meta': {'object_name': 'Instrument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"})
        },
        'mambomsapp.ionizationmode': {
            'Meta': {'object_name': 'IonizationMode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mambomsapp.lcmarecord': {
            'Meta': {'object_name': 'LCMARecord'},
            'biological_systems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mambomsapp.BiologicalSystem']", 'symmetrical': 'False'}),
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Column']"}),
            'compound_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mambomsapp.Compound']", 'unique': 'True', 'primary_key': 'True'}),
            'extract_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Instrument']"}),
            'kegg_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'kegg_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'known': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metabolite_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.MetaboliteClass']"}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.LCMethod']"}),
            'mono_isotopic_mass': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"}),
            'record_uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lcmarecord_uploaded_records'", 'to': "orm['auth.User']"}),
            'record_uploaded_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'record_vets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'lcmarecord_vetted_records'", 'symmetrical': 'False', 'through': "orm['mambomsapp.MARecordVet']", 'to': "orm['auth.User']"}),
            'retention_index': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'retention_time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sample_run_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lcmarecord_ran'", 'to': "orm['auth.User']"}),
            'structure': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'})
        },
        'mambomsapp.lcmethod': {
            'Meta': {'object_name': 'LCMethod'},
            'chromatography_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.ChromatographyType']"}),
            'derivitization_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'flow_rate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_method': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True'}),
            'ionization_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.IonizationMode']"}),
            'mass_range_acquired': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method_summary': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True'}),
            'ms_geometry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.MSGeometry']"}),
            'mz_exp_deriv_adducts': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Node']"}),
            'polarity': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'solvent_composition_a': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'solvent_composition_b': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'solvent_composition_c': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'solvent_composition_d': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.lcmodification': {
            'Meta': {'object_name': 'LCModification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'molecular_formula': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_of_compound': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.marecordvet': {
            'Meta': {'object_name': 'MARecordVet'},
            'gc_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.GCMARecord']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lc_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.LCMARecord']", 'null': 'True'}),
            'record_vetted_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mambomsapp.massspectratype': {
            'Meta': {'object_name': 'MassSpectraType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.metaboliteclass': {
            'Meta': {'object_name': 'MetaboliteClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mambomsapp.msgeometry': {
            'Meta': {'object_name': 'MSGeometry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mambomsapp.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mambomsapp.precursorselection': {
            'Meta': {'object_name': 'PrecursorSelection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'mambomsapp.precursortype': {
            'Meta': {'object_name': 'PrecursorType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'polarity': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'mambomsapp.spectrum': {
            'Meta': {'object_name': 'Spectrum'},
            'collison_energy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'compound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.Compound']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fragment_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ionized_species': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mambomsapp.LCModification']", 'null': 'True', 'blank': 'True'}),
            'mass_spectra_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.MassSpectraType']", 'null': 'True', 'blank': 'True'}),
            'precursor_ion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'precursor_mass': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '18', 'decimal_places': '10'}),
            'precursor_selection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.PrecursorSelection']", 'null': 'True', 'blank': 'True'}),
            'precursor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsapp.PrecursorType']", 'null': 'True', 'blank': 'True'}),
            'product_ion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'raw_points': ('django.db.models.fields.TextField', [], {})
        },
        'mambomsapp.synonym': {
            'Meta': {'object_name': 'Synonym'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ma_record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['mambomsapp.Compound']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['mambomsapp']
