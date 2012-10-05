# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        import datetime
        from decimal import Decimal

        mambomsapp_dataset_1 = orm['mambomsapp.dataset']()
        mambomsapp_dataset_1.name = u'NIST'
        mambomsapp_dataset_1.description = u'As imported from the NIST 2008 data file'
        mambomsapp_dataset_1.save()

        mambomsapp_dataset_2 = orm['mambomsapp.dataset']()
        mambomsapp_dataset_2.name = u'MA GC'
        mambomsapp_dataset_2.description = u'MA GC metabolite records'
        mambomsapp_dataset_2.save()

        mambomsapp_dataset_3 = orm['mambomsapp.dataset']()
        mambomsapp_dataset_3.name = u'MA LC'
        mambomsapp_dataset_3.description = u'MA LC metabolite records'
        mambomsapp_dataset_3.save()

        mambomsapp_node_1 = orm['mambomsapp.dataset']()
        mambomsapp_node_1.name = u'Test Node'
        mambomsapp_node_1.save()

        mambomsapp_precursortype_1 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_1.name = u'[M+H]+'
        mambomsapp_precursortype_1.polarity = u'P'
        mambomsapp_precursortype_1.save()

        mambomsapp_precursortype_2 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_2.name = u'[M+Na]+'
        mambomsapp_precursortype_2.polarity = u'P'
        mambomsapp_precursortype_2.save()

        mambomsapp_precursortype_3 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_3.name = u'[M+K]+'
        mambomsapp_precursortype_3.polarity = u'P'
        mambomsapp_precursortype_3.save()

        mambomsapp_precursortype_4 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_4.name = u'[M-H20+H]+'
        mambomsapp_precursortype_4.polarity = u'P'
        mambomsapp_precursortype_4.save()

        mambomsapp_precursortype_5 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_5.name = u'[M-H]-'
        mambomsapp_precursortype_5.polarity = u'N'
        mambomsapp_precursortype_5.save()

        mambomsapp_precursortype_6 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_6.name = u'[M+FA-H]-'
        mambomsapp_precursortype_6.polarity = u'N'
        mambomsapp_precursortype_6.save()

        mambomsapp_precursortype_7 = orm['mambomsapp.precursortype']()
        mambomsapp_precursortype_7.name = u'[M+HAc-H]-'
        mambomsapp_precursortype_7.polarity = u'N'
        mambomsapp_precursortype_7.save()

        mambomsapp_precursorselection_1 = orm['mambomsapp.precursorselection']()
        mambomsapp_precursorselection_1.name = u'Quadrupole'
        mambomsapp_precursorselection_1.save()

        mambomsapp_precursorselection_2 = orm['mambomsapp.precursorselection']()
        mambomsapp_precursorselection_2.name = u'Paul Trap'
        mambomsapp_precursorselection_2.save()

        mambomsapp_precursorselection_3 = orm['mambomsapp.precursorselection']()
        mambomsapp_precursorselection_3.name = u'ISCID'
        mambomsapp_precursorselection_3.save()


    def backwards(self, orm):
        "Write your backwards methods here."


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
