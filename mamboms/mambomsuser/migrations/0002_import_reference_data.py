# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):

        import datetime
        from decimal import Decimal
        '''
        #from django.contrib.contenttypes.models import ContentType
        
        #from django.contrib.auth.models import Permission
        print 'first contenttype'
        django_content_type_1 = orm['contenttypes.contenttype']()
        django_content_type_1.name = u'biological system'
        django_content_type_1.app_label = u'mambomsapp'
        django_content_type_1.model = u'biologicalsystem'
        django_content_type_1.save()
        print 'imported 1 contenttype'
        django_content_type_2 = orm['contenttypes.contenttype']()
        django_content_type_2.name = u'chromatography type'
        django_content_type_2.app_label = u'mambomsapp'
        django_content_type_2.model = u'chromatographytype'
        django_content_type_2.save()
        print 'imported 2 contenttype'

        django_content_type_3 = orm['contenttypes.contenttype']()
        django_content_type_3.name = u'column'
        django_content_type_3.app_label = u'mambomsapp'
        django_content_type_3.model = u'column'
        django_content_type_3.save()

        django_content_type_4 = orm['contenttypes.contenttype']()
        django_content_type_4.name = u'compound'
        django_content_type_4.app_label = u'mambomsapp'
        django_content_type_4.model = u'compound'
        django_content_type_4.save()

        django_content_type_5 = orm['contenttypes.contenttype']()
        django_content_type_5.name = u'content type'
        django_content_type_5.app_label = u'contenttypes'
        django_content_type_5.model = u'contenttype'
        django_content_type_5.save()

        django_content_type_6 = orm['contenttypes.contenttype']()
        django_content_type_6.name = u'dataset'
        django_content_type_6.app_label = u'mambomsapp'
        django_content_type_6.model = u'dataset'
        django_content_type_6.save()

        django_content_type_7 = orm['contenttypes.contenttype']()
        django_content_type_7.name = u'GC MA Record'
        django_content_type_7.app_label = u'mambomsapp'
        django_content_type_7.model = u'gcmarecord'
        django_content_type_7.save()

        django_content_type_8 = orm['contenttypes.contenttype']()
        django_content_type_8.name = u'GC Method'
        django_content_type_8.app_label = u'mambomsapp'
        django_content_type_8.model = u'gcmethod'
        django_content_type_8.save()

        django_content_type_9 = orm['contenttypes.contenttype']()
        django_content_type_9.name = u'group'
        django_content_type_9.app_label = u'auth'
        django_content_type_9.model = u'group'
        django_content_type_9.save()

        django_content_type_10 = orm['contenttypes.contenttype']()
        django_content_type_10.name = u'hash maintenance'
        django_content_type_10.app_label = u'mambomsapp'
        django_content_type_10.model = u'hashmaintenance'
        django_content_type_10.save()

        django_content_type_11 = orm['contenttypes.contenttype']()
        django_content_type_11.name = u'instrument'
        django_content_type_11.app_label = u'mambomsapp'
        django_content_type_11.model = u'instrument'
        django_content_type_11.save()

        django_content_type_12 = orm['contenttypes.contenttype']()
        django_content_type_12.name = u'ionization mode'
        django_content_type_12.app_label = u'mambomsapp'
        django_content_type_12.model = u'ionizationmode'
        django_content_type_12.save()

        django_content_type_13 = orm['contenttypes.contenttype']()
        django_content_type_13.name = u'LC MA Record'
        django_content_type_13.app_label = u'mambomsapp'
        django_content_type_13.model = u'lcmarecord'
        django_content_type_13.save()

        django_content_type_14 = orm['contenttypes.contenttype']()
        django_content_type_14.name = u'LC Method'
        django_content_type_14.app_label = u'mambomsapp'
        django_content_type_14.model = u'lcmethod'
        django_content_type_14.save()

        django_content_type_15 = orm['contenttypes.contenttype']()
        django_content_type_15.name = u'LC Modification'
        django_content_type_15.app_label = u'mambomsapp'
        django_content_type_15.model = u'lcmodification'
        django_content_type_15.save()

        django_content_type_16 = orm['contenttypes.contenttype']()
        django_content_type_16.name = u'log entry'
        django_content_type_16.app_label = u'admin'
        django_content_type_16.model = u'logentry'
        django_content_type_16.save()

        django_content_type_17 = orm['contenttypes.contenttype']()
        django_content_type_17.name = u'mamboms ldap profile'
        django_content_type_17.app_label = u'mambomsuser'
        django_content_type_17.model = u'mambomsldapprofile'
        django_content_type_17.save()

        django_content_type_18 = orm['contenttypes.contenttype']()
        django_content_type_18.name = u'ma record vet'
        django_content_type_18.app_label = u'mambomsapp'
        django_content_type_18.model = u'marecordvet'
        django_content_type_18.save()

        django_content_type_19 = orm['contenttypes.contenttype']()
        django_content_type_19.name = u'mass spectra type'
        django_content_type_19.app_label = u'mambomsapp'
        django_content_type_19.model = u'massspectratype'
        django_content_type_19.save()

        django_content_type_20 = orm['contenttypes.contenttype']()
        django_content_type_20.name = u'message'
        django_content_type_20.app_label = u'auth'
        django_content_type_20.model = u'message'
        django_content_type_20.save()

        django_content_type_21 = orm['contenttypes.contenttype']()
        django_content_type_21.name = u'metabolite class'
        django_content_type_21.app_label = u'mambomsapp'
        django_content_type_21.model = u'metaboliteclass'
        django_content_type_21.save()

        django_content_type_22 = orm['contenttypes.contenttype']()
        django_content_type_22.name = u'migration history'
        django_content_type_22.app_label = u'south'
        django_content_type_22.model = u'migrationhistory'
        django_content_type_22.save()

        django_content_type_23 = orm['contenttypes.contenttype']()
        django_content_type_23.name = u'MS Geometry'
        django_content_type_23.app_label = u'mambomsapp'
        django_content_type_23.model = u'msgeometry'
        django_content_type_23.save()

        django_content_type_24 = orm['contenttypes.contenttype']()
        django_content_type_24.name = u'node'
        django_content_type_24.app_label = u'mambomsapp'
        django_content_type_24.model = u'node'
        django_content_type_24.save()

        django_content_type_25 = orm['contenttypes.contenttype']()
        django_content_type_25.name = u'permission'
        django_content_type_25.app_label = u'auth'
        django_content_type_25.model = u'permission'
        django_content_type_25.save()

        django_content_type_26 = orm['contenttypes.contenttype']()
        django_content_type_26.name = u'precursor selection'
        django_content_type_26.app_label = u'mambomsapp'
        django_content_type_26.model = u'precursorselection'
        django_content_type_26.save()

        django_content_type_27 = orm['contenttypes.contenttype']()
        django_content_type_27.name = u'precursor type'
        django_content_type_27.app_label = u'mambomsapp'
        django_content_type_27.model = u'precursortype'
        django_content_type_27.save()

        django_content_type_28 = orm['contenttypes.contenttype']()
        django_content_type_28.name = u'spectrum'
        django_content_type_28.app_label = u'mambomsapp'
        django_content_type_28.model = u'spectrum'
        django_content_type_28.save()

        django_content_type_29 = orm['contenttypes.contenttype']()
        django_content_type_29.name = u'synonym'
        django_content_type_29.app_label = u'mambomsapp'
        django_content_type_29.model = u'synonym'
        django_content_type_29.save()

        django_content_type_30 = orm['contenttypes.contenttype']()
        django_content_type_30.name = u'user'
        django_content_type_30.app_label = u'auth'
        django_content_type_30.model = u'user'
        django_content_type_30.save()

        django_content_type_31 = orm['contenttypes.contenttype']()
        django_content_type_31.name = u'user status'
        django_content_type_31.app_label = u'mambomsuser'
        django_content_type_31.model = u'userstatus'
        django_content_type_31.save()
        


        auth_permission_1 = orm['auth.permission']()
        auth_permission_1.name = u'Can add log entry'
        auth_permission_1.content_type = ContentType.objects.get(app_label="admin", model="logentry")
        auth_permission_1.codename = u'add_logentry'
        auth_permission_1.save()

        print 'imported'

        auth_permission_2 = orm['auth.permission']()
        auth_permission_2.name = u'Can change log entry'
        auth_permission_2.content_type = ContentType.objects.get(app_label="admin", model="logentry")
        auth_permission_2.codename = u'change_logentry'
        auth_permission_2.save()

        auth_permission_3 = orm['auth.permission']()
        auth_permission_3.name = u'Can delete log entry'
        auth_permission_3.content_type = ContentType.objects.get(app_label="admin", model="logentry")
        auth_permission_3.codename = u'delete_logentry'
        auth_permission_3.save()

        auth_permission_4 = orm['auth.permission']()
        auth_permission_4.name = u'Can add group'
        auth_permission_4.content_type = ContentType.objects.get(app_label="auth", model="group")
        auth_permission_4.codename = u'add_group'
        auth_permission_4.save()

        auth_permission_5 = orm['auth.permission']()
        auth_permission_5.name = u'Can change group'
        auth_permission_5.content_type = ContentType.objects.get(app_label="auth", model="group")
        auth_permission_5.codename = u'change_group'
        auth_permission_5.save()

        auth_permission_6 = orm['auth.permission']()
        auth_permission_6.name = u'Can delete group'
        auth_permission_6.content_type = ContentType.objects.get(app_label="auth", model="group")
        auth_permission_6.codename = u'delete_group'
        auth_permission_6.save()

        auth_permission_7 = orm['auth.permission']()
        auth_permission_7.name = u'Can add message'
        auth_permission_7.content_type = ContentType.objects.get(app_label="auth", model="message")
        auth_permission_7.codename = u'add_message'
        auth_permission_7.save()

        auth_permission_8 = orm['auth.permission']()
        auth_permission_8.name = u'Can change message'
        auth_permission_8.content_type = ContentType.objects.get(app_label="auth", model="message")
        auth_permission_8.codename = u'change_message'
        auth_permission_8.save()

        auth_permission_9 = orm['auth.permission']()
        auth_permission_9.name = u'Can delete message'
        auth_permission_9.content_type = ContentType.objects.get(app_label="auth", model="message")
        auth_permission_9.codename = u'delete_message'
        auth_permission_9.save()

        auth_permission_10 = orm['auth.permission']()
        auth_permission_10.name = u'Can add permission'
        auth_permission_10.content_type = ContentType.objects.get(app_label="auth", model="permission")
        auth_permission_10.codename = u'add_permission'
        auth_permission_10.save()

        auth_permission_11 = orm['auth.permission']()
        auth_permission_11.name = u'Can change permission'
        auth_permission_11.content_type = ContentType.objects.get(app_label="auth", model="permission")
        auth_permission_11.codename = u'change_permission'
        auth_permission_11.save()

        auth_permission_12 = orm['auth.permission']()
        auth_permission_12.name = u'Can delete permission'
        auth_permission_12.content_type = ContentType.objects.get(app_label="auth", model="permission")
        auth_permission_12.codename = u'delete_permission'
        auth_permission_12.save()

        auth_permission_13 = orm['auth.permission']()
        auth_permission_13.name = u'Can add user'
        auth_permission_13.content_type = ContentType.objects.get(app_label="auth", model="user")
        auth_permission_13.codename = u'add_user'
        auth_permission_13.save()

        auth_permission_14 = orm['auth.permission']()
        auth_permission_14.name = u'Can change user'
        auth_permission_14.content_type = ContentType.objects.get(app_label="auth", model="user")
        auth_permission_14.codename = u'change_user'
        auth_permission_14.save()

        auth_permission_15 = orm['auth.permission']()
        auth_permission_15.name = u'Can delete user'
        auth_permission_15.content_type = ContentType.objects.get(app_label="auth", model="user")
        auth_permission_15.codename = u'delete_user'
        auth_permission_15.save()

        auth_permission_16 = orm['auth.permission']()
        auth_permission_16.name = u'Can add content type'
        auth_permission_16.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
        auth_permission_16.codename = u'add_contenttype'
        auth_permission_16.save()

        auth_permission_17 = orm['auth.permission']()
        auth_permission_17.name = u'Can change content type'
        auth_permission_17.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
        auth_permission_17.codename = u'change_contenttype'
        auth_permission_17.save()

        auth_permission_18 = orm['auth.permission']()
        auth_permission_18.name = u'Can delete content type'
        auth_permission_18.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
        auth_permission_18.codename = u'delete_contenttype'
        auth_permission_18.save()

        auth_permission_19 = orm['auth.permission']()
        auth_permission_19.name = u'Can add biological system'
        auth_permission_19.content_type = ContentType.objects.get(app_label="mambomsapp", model="biologicalsystem")
        auth_permission_19.codename = u'add_biologicalsystem'
        auth_permission_19.save()

        auth_permission_20 = orm['auth.permission']()
        auth_permission_20.name = u'Can change biological system'
        auth_permission_20.content_type = ContentType.objects.get(app_label="mambomsapp", model="biologicalsystem")
        auth_permission_20.codename = u'change_biologicalsystem'
        auth_permission_20.save()

        auth_permission_21 = orm['auth.permission']()
        auth_permission_21.name = u'Can delete biological system'
        auth_permission_21.content_type = ContentType.objects.get(app_label="mambomsapp", model="biologicalsystem")
        auth_permission_21.codename = u'delete_biologicalsystem'
        auth_permission_21.save()

        auth_permission_22 = orm['auth.permission']()
        auth_permission_22.name = u'Can add chromatography type'
        auth_permission_22.content_type = ContentType.objects.get(app_label="mambomsapp", model="chromatographytype")
        auth_permission_22.codename = u'add_chromatographytype'
        auth_permission_22.save()

        auth_permission_23 = orm['auth.permission']()
        auth_permission_23.name = u'Can change chromatography type'
        auth_permission_23.content_type = ContentType.objects.get(app_label="mambomsapp", model="chromatographytype")
        auth_permission_23.codename = u'change_chromatographytype'
        auth_permission_23.save()

        auth_permission_24 = orm['auth.permission']()
        auth_permission_24.name = u'Can delete chromatography type'
        auth_permission_24.content_type = ContentType.objects.get(app_label="mambomsapp", model="chromatographytype")
        auth_permission_24.codename = u'delete_chromatographytype'
        auth_permission_24.save()

        auth_permission_25 = orm['auth.permission']()
        auth_permission_25.name = u'Can add column'
        auth_permission_25.content_type = ContentType.objects.get(app_label="mambomsapp", model="column")
        auth_permission_25.codename = u'add_column'
        auth_permission_25.save()

        auth_permission_26 = orm['auth.permission']()
        auth_permission_26.name = u'Can change column'
        auth_permission_26.content_type = ContentType.objects.get(app_label="mambomsapp", model="column")
        auth_permission_26.codename = u'change_column'
        auth_permission_26.save()

        auth_permission_27 = orm['auth.permission']()
        auth_permission_27.name = u'Can delete column'
        auth_permission_27.content_type = ContentType.objects.get(app_label="mambomsapp", model="column")
        auth_permission_27.codename = u'delete_column'
        auth_permission_27.save()

        auth_permission_28 = orm['auth.permission']()
        auth_permission_28.name = u'Can add compound'
        auth_permission_28.content_type = ContentType.objects.get(app_label="mambomsapp", model="compound")
        auth_permission_28.codename = u'add_compound'
        auth_permission_28.save()

        auth_permission_29 = orm['auth.permission']()
        auth_permission_29.name = u'Can change compound'
        auth_permission_29.content_type = ContentType.objects.get(app_label="mambomsapp", model="compound")
        auth_permission_29.codename = u'change_compound'
        auth_permission_29.save()

        auth_permission_30 = orm['auth.permission']()
        auth_permission_30.name = u'Can delete compound'
        auth_permission_30.content_type = ContentType.objects.get(app_label="mambomsapp", model="compound")
        auth_permission_30.codename = u'delete_compound'
        auth_permission_30.save()

        auth_permission_31 = orm['auth.permission']()
        auth_permission_31.name = u'Can add dataset'
        auth_permission_31.content_type = ContentType.objects.get(app_label="mambomsapp", model="dataset")
        auth_permission_31.codename = u'add_dataset'
        auth_permission_31.save()

        auth_permission_32 = orm['auth.permission']()
        auth_permission_32.name = u'Can change dataset'
        auth_permission_32.content_type = ContentType.objects.get(app_label="mambomsapp", model="dataset")
        auth_permission_32.codename = u'change_dataset'
        auth_permission_32.save()

        auth_permission_33 = orm['auth.permission']()
        auth_permission_33.name = u'Can delete dataset'
        auth_permission_33.content_type = ContentType.objects.get(app_label="mambomsapp", model="dataset")
        auth_permission_33.codename = u'delete_dataset'
        auth_permission_33.save()

        auth_permission_34 = orm['auth.permission']()
        auth_permission_34.name = u'Can add GC MA Record'
        auth_permission_34.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmarecord")
        auth_permission_34.codename = u'add_gcmarecord'
        auth_permission_34.save()

        auth_permission_35 = orm['auth.permission']()
        auth_permission_35.name = u'Can change GC MA Record'
        auth_permission_35.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmarecord")
        auth_permission_35.codename = u'change_gcmarecord'
        auth_permission_35.save()

        auth_permission_36 = orm['auth.permission']()
        auth_permission_36.name = u'Can delete GC MA Record'
        auth_permission_36.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmarecord")
        auth_permission_36.codename = u'delete_gcmarecord'
        auth_permission_36.save()

        auth_permission_37 = orm['auth.permission']()
        auth_permission_37.name = u'Can add GC Method'
        auth_permission_37.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmethod")
        auth_permission_37.codename = u'add_gcmethod'
        auth_permission_37.save()

        auth_permission_38 = orm['auth.permission']()
        auth_permission_38.name = u'Can change GC Method'
        auth_permission_38.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmethod")
        auth_permission_38.codename = u'change_gcmethod'
        auth_permission_38.save()

        auth_permission_39 = orm['auth.permission']()
        auth_permission_39.name = u'Can delete GC Method'
        auth_permission_39.content_type = ContentType.objects.get(app_label="mambomsapp", model="gcmethod")
        auth_permission_39.codename = u'delete_gcmethod'
        auth_permission_39.save()

        auth_permission_40 = orm['auth.permission']()
        auth_permission_40.name = u'Can add hash maintenance'
        auth_permission_40.content_type = ContentType.objects.get(app_label="mambomsapp", model="hashmaintenance")
        auth_permission_40.codename = u'add_hashmaintenance'
        auth_permission_40.save()

        auth_permission_41 = orm['auth.permission']()
        auth_permission_41.name = u'Can change hash maintenance'
        auth_permission_41.content_type = ContentType.objects.get(app_label="mambomsapp", model="hashmaintenance")
        auth_permission_41.codename = u'change_hashmaintenance'
        auth_permission_41.save()

        auth_permission_42 = orm['auth.permission']()
        auth_permission_42.name = u'Can delete hash maintenance'
        auth_permission_42.content_type = ContentType.objects.get(app_label="mambomsapp", model="hashmaintenance")
        auth_permission_42.codename = u'delete_hashmaintenance'
        auth_permission_42.save()

        auth_permission_43 = orm['auth.permission']()
        auth_permission_43.name = u'Can add instrument'
        auth_permission_43.content_type = ContentType.objects.get(app_label="mambomsapp", model="instrument")
        auth_permission_43.codename = u'add_instrument'
        auth_permission_43.save()

        auth_permission_44 = orm['auth.permission']()
        auth_permission_44.name = u'Can change instrument'
        auth_permission_44.content_type = ContentType.objects.get(app_label="mambomsapp", model="instrument")
        auth_permission_44.codename = u'change_instrument'
        auth_permission_44.save()

        auth_permission_45 = orm['auth.permission']()
        auth_permission_45.name = u'Can delete instrument'
        auth_permission_45.content_type = ContentType.objects.get(app_label="mambomsapp", model="instrument")
        auth_permission_45.codename = u'delete_instrument'
        auth_permission_45.save()

        auth_permission_46 = orm['auth.permission']()
        auth_permission_46.name = u'Can add ionization mode'
        auth_permission_46.content_type = ContentType.objects.get(app_label="mambomsapp", model="ionizationmode")
        auth_permission_46.codename = u'add_ionizationmode'
        auth_permission_46.save()

        auth_permission_47 = orm['auth.permission']()
        auth_permission_47.name = u'Can change ionization mode'
        auth_permission_47.content_type = ContentType.objects.get(app_label="mambomsapp", model="ionizationmode")
        auth_permission_47.codename = u'change_ionizationmode'
        auth_permission_47.save()

        auth_permission_48 = orm['auth.permission']()
        auth_permission_48.name = u'Can delete ionization mode'
        auth_permission_48.content_type = ContentType.objects.get(app_label="mambomsapp", model="ionizationmode")
        auth_permission_48.codename = u'delete_ionizationmode'
        auth_permission_48.save()

        auth_permission_49 = orm['auth.permission']()
        auth_permission_49.name = u'Can add LC MA Record'
        auth_permission_49.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmarecord")
        auth_permission_49.codename = u'add_lcmarecord'
        auth_permission_49.save()

        auth_permission_50 = orm['auth.permission']()
        auth_permission_50.name = u'Can change LC MA Record'
        auth_permission_50.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmarecord")
        auth_permission_50.codename = u'change_lcmarecord'
        auth_permission_50.save()

        auth_permission_51 = orm['auth.permission']()
        auth_permission_51.name = u'Can delete LC MA Record'
        auth_permission_51.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmarecord")
        auth_permission_51.codename = u'delete_lcmarecord'
        auth_permission_51.save()

        auth_permission_52 = orm['auth.permission']()
        auth_permission_52.name = u'Can add LC Method'
        auth_permission_52.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmethod")
        auth_permission_52.codename = u'add_lcmethod'
        auth_permission_52.save()

        auth_permission_53 = orm['auth.permission']()
        auth_permission_53.name = u'Can change LC Method'
        auth_permission_53.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmethod")
        auth_permission_53.codename = u'change_lcmethod'
        auth_permission_53.save()

        auth_permission_54 = orm['auth.permission']()
        auth_permission_54.name = u'Can delete LC Method'
        auth_permission_54.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmethod")
        auth_permission_54.codename = u'delete_lcmethod'
        auth_permission_54.save()

        auth_permission_55 = orm['auth.permission']()
        auth_permission_55.name = u'Can add LC Modification'
        auth_permission_55.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmodification")
        auth_permission_55.codename = u'add_lcmodification'
        auth_permission_55.save()

        auth_permission_56 = orm['auth.permission']()
        auth_permission_56.name = u'Can change LC Modification'
        auth_permission_56.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmodification")
        auth_permission_56.codename = u'change_lcmodification'
        auth_permission_56.save()

        auth_permission_57 = orm['auth.permission']()
        auth_permission_57.name = u'Can delete LC Modification'
        auth_permission_57.content_type = ContentType.objects.get(app_label="mambomsapp", model="lcmodification")
        auth_permission_57.codename = u'delete_lcmodification'
        auth_permission_57.save()

        auth_permission_58 = orm['auth.permission']()
        auth_permission_58.name = u'Can add ma record vet'
        auth_permission_58.content_type = ContentType.objects.get(app_label="mambomsapp", model="marecordvet")
        auth_permission_58.codename = u'add_marecordvet'
        auth_permission_58.save()

        auth_permission_59 = orm['auth.permission']()
        auth_permission_59.name = u'Can change ma record vet'
        auth_permission_59.content_type = ContentType.objects.get(app_label="mambomsapp", model="marecordvet")
        auth_permission_59.codename = u'change_marecordvet'
        auth_permission_59.save()

        auth_permission_60 = orm['auth.permission']()
        auth_permission_60.name = u'Can delete ma record vet'
        auth_permission_60.content_type = ContentType.objects.get(app_label="mambomsapp", model="marecordvet")
        auth_permission_60.codename = u'delete_marecordvet'
        auth_permission_60.save()

        auth_permission_61 = orm['auth.permission']()
        auth_permission_61.name = u'Can add mass spectra type'
        auth_permission_61.content_type = ContentType.objects.get(app_label="mambomsapp", model="massspectratype")
        auth_permission_61.codename = u'add_massspectratype'
        auth_permission_61.save()

        auth_permission_62 = orm['auth.permission']()
        auth_permission_62.name = u'Can change mass spectra type'
        auth_permission_62.content_type = ContentType.objects.get(app_label="mambomsapp", model="massspectratype")
        auth_permission_62.codename = u'change_massspectratype'
        auth_permission_62.save()

        auth_permission_63 = orm['auth.permission']()
        auth_permission_63.name = u'Can delete mass spectra type'
        auth_permission_63.content_type = ContentType.objects.get(app_label="mambomsapp", model="massspectratype")
        auth_permission_63.codename = u'delete_massspectratype'
        auth_permission_63.save()

        auth_permission_64 = orm['auth.permission']()
        auth_permission_64.name = u'Can add metabolite class'
        auth_permission_64.content_type = ContentType.objects.get(app_label="mambomsapp", model="metaboliteclass")
        auth_permission_64.codename = u'add_metaboliteclass'
        auth_permission_64.save()

        auth_permission_65 = orm['auth.permission']()
        auth_permission_65.name = u'Can change metabolite class'
        auth_permission_65.content_type = ContentType.objects.get(app_label="mambomsapp", model="metaboliteclass")
        auth_permission_65.codename = u'change_metaboliteclass'
        auth_permission_65.save()

        auth_permission_66 = orm['auth.permission']()
        auth_permission_66.name = u'Can delete metabolite class'
        auth_permission_66.content_type = ContentType.objects.get(app_label="mambomsapp", model="metaboliteclass")
        auth_permission_66.codename = u'delete_metaboliteclass'
        auth_permission_66.save()

        auth_permission_67 = orm['auth.permission']()
        auth_permission_67.name = u'Can add MS Geometry'
        auth_permission_67.content_type = ContentType.objects.get(app_label="mambomsapp", model="msgeometry")
        auth_permission_67.codename = u'add_msgeometry'
        auth_permission_67.save()

        auth_permission_68 = orm['auth.permission']()
        auth_permission_68.name = u'Can change MS Geometry'
        auth_permission_68.content_type = ContentType.objects.get(app_label="mambomsapp", model="msgeometry")
        auth_permission_68.codename = u'change_msgeometry'
        auth_permission_68.save()

        auth_permission_69 = orm['auth.permission']()
        auth_permission_69.name = u'Can delete MS Geometry'
        auth_permission_69.content_type = ContentType.objects.get(app_label="mambomsapp", model="msgeometry")
        auth_permission_69.codename = u'delete_msgeometry'
        auth_permission_69.save()

        auth_permission_70 = orm['auth.permission']()
        auth_permission_70.name = u'Can add node'
        auth_permission_70.content_type = ContentType.objects.get(app_label="mambomsapp", model="node")
        auth_permission_70.codename = u'add_node'
        auth_permission_70.save()

        auth_permission_71 = orm['auth.permission']()
        auth_permission_71.name = u'Can change node'
        auth_permission_71.content_type = ContentType.objects.get(app_label="mambomsapp", model="node")
        auth_permission_71.codename = u'change_node'
        auth_permission_71.save()

        auth_permission_72 = orm['auth.permission']()
        auth_permission_72.name = u'Can delete node'
        auth_permission_72.content_type = ContentType.objects.get(app_label="mambomsapp", model="node")
        auth_permission_72.codename = u'delete_node'
        auth_permission_72.save()

        auth_permission_73 = orm['auth.permission']()
        auth_permission_73.name = u'Can add precursor selection'
        auth_permission_73.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursorselection")
        auth_permission_73.codename = u'add_precursorselection'
        auth_permission_73.save()

        auth_permission_74 = orm['auth.permission']()
        auth_permission_74.name = u'Can change precursor selection'
        auth_permission_74.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursorselection")
        auth_permission_74.codename = u'change_precursorselection'
        auth_permission_74.save()

        auth_permission_75 = orm['auth.permission']()
        auth_permission_75.name = u'Can delete precursor selection'
        auth_permission_75.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursorselection")
        auth_permission_75.codename = u'delete_precursorselection'
        auth_permission_75.save()

        auth_permission_76 = orm['auth.permission']()
        auth_permission_76.name = u'Can add precursor type'
        auth_permission_76.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursortype")
        auth_permission_76.codename = u'add_precursortype'
        auth_permission_76.save()

        auth_permission_77 = orm['auth.permission']()
        auth_permission_77.name = u'Can change precursor type'
        auth_permission_77.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursortype")
        auth_permission_77.codename = u'change_precursortype'
        auth_permission_77.save()

        auth_permission_78 = orm['auth.permission']()
        auth_permission_78.name = u'Can delete precursor type'
        auth_permission_78.content_type = ContentType.objects.get(app_label="mambomsapp", model="precursortype")
        auth_permission_78.codename = u'delete_precursortype'
        auth_permission_78.save()

        auth_permission_79 = orm['auth.permission']()
        auth_permission_79.name = u'Can add spectrum'
        auth_permission_79.content_type = ContentType.objects.get(app_label="mambomsapp", model="spectrum")
        auth_permission_79.codename = u'add_spectrum'
        auth_permission_79.save()

        auth_permission_80 = orm['auth.permission']()
        auth_permission_80.name = u'Can change spectrum'
        auth_permission_80.content_type = ContentType.objects.get(app_label="mambomsapp", model="spectrum")
        auth_permission_80.codename = u'change_spectrum'
        auth_permission_80.save()

        auth_permission_81 = orm['auth.permission']()
        auth_permission_81.name = u'Can delete spectrum'
        auth_permission_81.content_type = ContentType.objects.get(app_label="mambomsapp", model="spectrum")
        auth_permission_81.codename = u'delete_spectrum'
        auth_permission_81.save()

        auth_permission_82 = orm['auth.permission']()
        auth_permission_82.name = u'Can add synonym'
        auth_permission_82.content_type = ContentType.objects.get(app_label="mambomsapp", model="synonym")
        auth_permission_82.codename = u'add_synonym'
        auth_permission_82.save()

        auth_permission_83 = orm['auth.permission']()
        auth_permission_83.name = u'Can change synonym'
        auth_permission_83.content_type = ContentType.objects.get(app_label="mambomsapp", model="synonym")
        auth_permission_83.codename = u'change_synonym'
        auth_permission_83.save()

        auth_permission_84 = orm['auth.permission']()
        auth_permission_84.name = u'Can delete synonym'
        auth_permission_84.content_type = ContentType.objects.get(app_label="mambomsapp", model="synonym")
        auth_permission_84.codename = u'delete_synonym'
        auth_permission_84.save()

        auth_permission_85 = orm['auth.permission']()
        auth_permission_85.name = u'Can add mamboms ldap profile'
        auth_permission_85.content_type = ContentType.objects.get(app_label="mambomsuser", model="mambomsldapprofile")
        auth_permission_85.codename = u'add_mambomsldapprofile'
        auth_permission_85.save()

        auth_permission_86 = orm['auth.permission']()
        auth_permission_86.name = u'Can change mamboms ldap profile'
        auth_permission_86.content_type = ContentType.objects.get(app_label="mambomsuser", model="mambomsldapprofile")
        auth_permission_86.codename = u'change_mambomsldapprofile'
        auth_permission_86.save()

        auth_permission_87 = orm['auth.permission']()
        auth_permission_87.name = u'Can delete mamboms ldap profile'
        auth_permission_87.content_type = ContentType.objects.get(app_label="mambomsuser", model="mambomsldapprofile")
        auth_permission_87.codename = u'delete_mambomsldapprofile'
        auth_permission_87.save()

        auth_permission_88 = orm['auth.permission']()
        auth_permission_88.name = u'Can add user status'
        auth_permission_88.content_type = ContentType.objects.get(app_label="mambomsuser", model="userstatus")
        auth_permission_88.codename = u'add_userstatus'
        auth_permission_88.save()

        auth_permission_89 = orm['auth.permission']()
        auth_permission_89.name = u'Can change user status'
        auth_permission_89.content_type = ContentType.objects.get(app_label="mambomsuser", model="userstatus")
        auth_permission_89.codename = u'change_userstatus'
        auth_permission_89.save()

        auth_permission_90 = orm['auth.permission']()
        auth_permission_90.name = u'Can delete user status'
        auth_permission_90.content_type = ContentType.objects.get(app_label="mambomsuser", model="userstatus")
        auth_permission_90.codename = u'delete_userstatus'
        auth_permission_90.save()

        auth_permission_91 = orm['auth.permission']()
        auth_permission_91.name = u'Can add migration history'
        auth_permission_91.content_type = ContentType.objects.get(app_label="south", model="migrationhistory")
        auth_permission_91.codename = u'add_migrationhistory'
        auth_permission_91.save()

        auth_permission_92 = orm['auth.permission']()
        auth_permission_92.name = u'Can change migration history'
        auth_permission_92.content_type = ContentType.objects.get(app_label="south", model="migrationhistory")
        auth_permission_92.codename = u'change_migrationhistory'
        auth_permission_92.save()

        auth_permission_93 = orm['auth.permission']()
        auth_permission_93.name = u'Can delete migration history'
        auth_permission_93.content_type = ContentType.objects.get(app_label="south", model="migrationhistory")
        auth_permission_93.codename = u'delete_migrationhistory'
        auth_permission_93.save()

        #from django.contrib.auth.models import Group
        '''

        auth_group_1 = orm['auth.group']()
        auth_group_1.name = u'NodeRep'
        auth_group_1.save()

        #from django.contrib.auth.models import User

        auth_user_1 = orm['auth.user']()
        auth_user_1.username = u'admin@mambo-ms.com'
        auth_user_1.first_name = u'Admin'
        auth_user_1.last_name = u'User'
        auth_user_1.email = u'admin@mambo-ms.com'
        auth_user_1.password = u'sha1$7f57a$97456404bf498ef0474fcc3209279255c9115610'
        auth_user_1.is_staff = True
        auth_user_1.is_active = True
        auth_user_1.is_superuser = True
        auth_user_1.last_login = datetime.datetime(2011, 5, 10, 14, 3, 44)
        auth_user_1.date_joined = datetime.datetime(2010, 5, 5, 11, 11, 27)
        auth_user_1.save()

        auth_user_1.groups.add(auth_group_1)

        mambomsuser_userstatus_1 = orm['mambomsuser.userstatus']()
        mambomsuser_userstatus_1.name = u'Active'
        mambomsuser_userstatus_1.save()

        mambomsuser_userstatus_2 = orm['mambomsuser.userstatus']()
        mambomsuser_userstatus_2.name = u'Pending'
        mambomsuser_userstatus_2.save()

        mambomsuser_userstatus_3 = orm['mambomsuser.userstatus']()
        mambomsuser_userstatus_3.name = u'Rejected'
        mambomsuser_userstatus_3.save()

        mambomsuser_userstatus_4 = orm['mambomsuser.userstatus']()
        mambomsuser_userstatus_4.name = u'Deleted'
        mambomsuser_userstatus_4.save()

        mambomsuser_mambomsldapprofile_1 = orm['mambomsuser.mambomsldapprofile']()
        mambomsuser_mambomsldapprofile_1.title = None
        mambomsuser_mambomsldapprofile_1.first_name = None
        mambomsuser_mambomsldapprofile_1.last_name = None
        mambomsuser_mambomsldapprofile_1.office = None
        mambomsuser_mambomsldapprofile_1.office_phone = None
        mambomsuser_mambomsldapprofile_1.home_phone = None
        mambomsuser_mambomsldapprofile_1.position = None
        mambomsuser_mambomsldapprofile_1.department = None
        mambomsuser_mambomsldapprofile_1.institute = None
        mambomsuser_mambomsldapprofile_1.address = None
        mambomsuser_mambomsldapprofile_1.supervisor = None
        mambomsuser_mambomsldapprofile_1.area_of_interest = None
        mambomsuser_mambomsldapprofile_1.country = None
        mambomsuser_mambomsldapprofile_1.password_reset_token = None
        mambomsuser_mambomsldapprofile_1.node = None
        mambomsuser_mambomsldapprofile_1.status = mambomsuser_userstatus_1
        #mambomsuser_mambomsldapprofile_1.save()
        mambomsuser_mambomsldapprofile_1.user__id = 1;

        mambomsuser_mambomsldapprofile_1.user = auth_user_1 
        mambomsuser_mambomsldapprofile_1.save()
        

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
        'mambomsapp.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mambomsuser.mambomsldapprofile': {
            'Meta': {'object_name': 'MambomsLDAPProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'area_of_interest': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['mambomsapp.Node']"}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'office_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'password_reset_token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mambomsuser.UserStatus']"}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'mambomsuser.userstatus': {
            'Meta': {'object_name': 'UserStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['mambomsuser']
