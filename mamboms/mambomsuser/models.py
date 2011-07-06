from django.db import models
from django.contrib.auth.models import User, Group, UserManager
from mamboms import LDAPHandler
from mamboms.utils import debugPrint as dprint
from mamboms import mambomsapp
from mamboms import settings

import base64
import hashlib
import uuid

NODEREP_GROUP_NAME = 'NodeRep'

dprint.register(True, 'mambomsuser.log')


PROFILE_PROPERTIES = {
    'firstname': 'first_name', 
    'lastname': 'last_name', 
    'telephoneNumber': 'office_phone',
    'homephone': 'home_phone', 
    'physicalDeliveryOfficeName': 'office', 
    'title': 'title', 
    'dept': 'department', 
    'areaOfInterest': 'area_of_interest',
    'address': 'address', 
    'institute': 'institute', 
    'supervisor': 'supervisor', 
    'country': 'country', 
    'node': 'node', 
    'status': 'status'
}


def extract_properties(obj, props):
    assert obj is not None
    d = {}
    for target_prop,source_prop in props.items():
        prop_value = getattr(obj, source_prop)
        if prop_value is not None:
            d[target_prop] = str(prop_value)
    return d

def set_properties(obj, props, dictionary):
    assert obj is not None
    for key, prop in props.items():
        value = dictionary.get(key)
        if value is not None:
            setattr(obj, prop, value)

def list_users():
    return [u.get_profile().get_details() for u in User.objects.all()]

def list_mamboms_nodes():
    return [ {"name": n.name, "id": n.id} for n in mambomsapp.models.Node.objects.all()]

class UserStatus(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class MambomsLDAPProfile(models.Model):
    user = models.ForeignKey(User, unique = True)
    title  = models.CharField(null=True,max_length=50)
    first_name  = models.CharField(null=True,max_length=50)
    last_name = models.CharField(null=True,max_length=50)
    office = models.CharField(null=True,max_length=50)
    office_phone = models.CharField(null=True,max_length=50)
    home_phone = models.CharField(null=True,max_length=50)
    position = models.CharField(null=True,max_length=50)
    department = models.CharField(null=True,max_length=50)
    institute = models.CharField(null=True,max_length=50)
    address = models.CharField(null=True,max_length=255)
    supervisor = models.CharField(null=True,max_length=50)
    area_of_interest = models.CharField(null=True,max_length=255)
    country = models.CharField(null=True,max_length=50)
    password_reset_token = models.CharField(null=True, db_index=True, max_length=50)

    node = models.ForeignKey('mambomsapp.Node', null=True)
    status = models.ForeignKey(UserStatus)

    def get_details(self):
        '''should return the internal details in a format palatable to the app'''
        returndict = extract_properties(self, PROFILE_PROPERTIES)
        returndict['email'] = self.user.username
        returndict['username'] = self.user.username
        returndict['originalEmail'] = self.user.username

        returndict['isAdmin'] = self.is_admin
        returndict['isNodeRep'] = self.is_noderep
        returndict['isClient'] = self.is_client
        dprint('get_details returning isAdmin: %s' % (str(returndict['isAdmin']) ) )
        dprint('get_details returning isNodeRep: %s' % (str(returndict['isNodeRep']) ) )
        
        return returndict

    def save_details(self, detailsDict, infoDict, updaterUser):
        # The detailsDict is a dictionary with key, value pairs of data to set. It should be 
        #   as close to the set of storable 'user attributes' as you can get, although some data massaging
        #   may need to take place before saving
        #   Blank values will be replaced with current values.
        # The infoDict contains any other information that the save function might need to make decisions
        #   about how to update and save the data. This is specific to the application - the frontend being used,
        #   the user attributes present on this type of user etc.
        # The updateUser is the user object of the person MAKING the update.
        #   This is so we know if that person was an admin, noderep etc, and therefore what 
        #   they are and are not allowed to update.

        dprint('***enter***')
        changed_details = False
   
        set_properties(self, PROFILE_PROPERTIES, detailsDict)        

        newnode = infoDict.get('node')
        if newnode:
            changed_details = True
            self.node = mambomsapp.models.Node.objects.get(id=newnode)

        if updaterUser.is_superuser:
            is_admin = infoDict.get('adminCheckbox')
            if is_admin is not None:
                self.user.is_superuser = is_admin
            is_noderep = infoDict.get('noderepCheckbox')
            if is_noderep is not None:
                noderepgroup = Group.objects.get(name=NODEREP_GROUP_NAME)
                if is_noderep:
                    self.user.groups.add(noderepgroup)
                else:
                    self.user.groups.remove(noderepgroup)

        print infoDict
        self.change_password(infoDict['password'])
       
        self.user.save()
        self.save()

        dprint('***exit***')
        return changed_details

    def change_password(self, new_password):
        if not new_password:
            return
        if True in [b.endswith('LDAPBackend') for b in settings.AUTHENTICATION_BACKENDS]:
            try:
                adminld = LDAPHandler(userdn = settings.LDAPADMINUSERNAME, password = settings.LDAPADMINPASSWORD)
                u = self.user.username
                adminld.ldap_update_user(u, u, new_password, {}, pwencoding='md5')
            except Exception, e:
                dprint('Exception updating %s: %s' % (str(u), str(e)) )
                raise 
        else:
           self.user.set_password(new_password)
           print 'Updated Django'

    def generate_password_reset_token(self):
        # There is a token generator in django.contrib.auth, but I'm not
        # terribly thrilled with the way it works: it relies on the user's last
        # login time being invariant, which isn't necessarily the case. We'll
        # use SECRET_KEY here as well, but with a dash more randomness via
        # UUID.
        hash = hashlib.sha256()
        hash.update(settings.SECRET_KEY)
        hash.update(uuid.uuid4().bytes)
        hash.update(self.user.username)

        return base64.urlsafe_b64encode(hash.digest())

    @property
    def is_noderep(self):
        try:
            self.user.groups.get(name=NODEREP_GROUP_NAME)
            return True
        except Group.DoesNotExist:
            return False
   
    @property
    def is_admin(self):
        return self.user.is_superuser
    
    @property
    def is_client(self):
        if self.is_admin or self.is_noderep:
            return False
        return (self.node is None)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

from django.db.models.signals import post_save
def mambomsuser_post_save(sender, instance, created, **kwargs):
    if created:
        prof = MambomsLDAPProfile(user=instance)
        prof.status = UserStatus.objects.get(name='Pending')
        prof.save()
post_save.connect(mambomsuser_post_save, sender=User)
