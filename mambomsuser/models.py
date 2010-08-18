from django.db import models
from django.contrib.auth.models import User, Group, UserManager
from mamboms import LDAPHandler
from mamboms.utils import debugPrint as dprint
from mamboms import mambomsapp
from mamboms import settings

NODEREP_GROUP_NAME = 'NodeRep'

MAMBOMS_STATUS_GROUPS = ('User', 'Pending', 'Deleted', 'Rejected')
MAMBOMS_ADMIN_GROUPS = ('Administrators', 'Node Reps')

dprint.register(True, 'mambomsuser.log')

#Here we put all the models and helper functions that are needed so that the user profile
#model can do its job, and transparently present the data which is in LDAP/Django

MAMBOMS_TO_LDAP_DICT = {
    'username': 'uid', 
    'commonname': 'commonName', 
    'firstname': 'givenName', 
    'lastname': 'sn', 
    'email': 'mail',
    'telephoneNumber': 'telephoneNumber',
    'homephone': 'homePhone',
    'physicalDeliveryOfficeName': 'physicalDeliveryOfficeName',
    'title': 'title', 
    'dept': 'destinationIndicator',
    'areaOfInterest': 'description',
    'address': 'postalAddress',
    'institute': 'businessCategory',
    'supervisor': 'registeredAddress',
    'country': 'carLicense'
}

# Inverse of MAMBOMS_TO_LDAP_DICT
LDAP_TO_MAMBOMS_DICT = dict(
    [(value, key) for key, value in MAMBOMS_TO_LDAP_DICT.items()])

def translate_mamboms_to_ldap(mdict):
    ''' Translates a dictionary holding data keyed against strings used in 
        the web application forms to the strings used in the LDAP store
        Expects a 'mamboms' dictionary,
        Returns a LDAP dictionary
    '''
    return dict( 
        [(MAMBOMS_TO_LDAP_DICT[key], value) for key, value in mdict.items() if MAMBOMS_TO_LDAP_DICT.has_key(key)]
    )

def translate_ldap_to_mamboms(ldict):
    ''' Translates a dictionary holding data keyed against strings used in 
        the ldap store to the strings used in the web application forms
        Expects a LDAP dictionary,
        Returns a 'mamboms' dictionary
    '''
    return dict(
        [(LDAP_TO_MAMBOMS_DICT[key], value) for key, value in ldict.items() if LDAP_TO_MAMBOMS_DICT.has_key(key)]
    )

def user_has_profile(user):
    try:
        user.get_profile()
        return True
    except MambomsLDAPProfile.DoesNotExist:
        return False

def list_users():
    try:
        ld = LDAPHandler()
        ul = ld.ldap_list_users( [settings.DEFAULT_GROUP] )
        return [translate_ldap_to_mamboms(entry) for entry in ul]
    finally:
        ld.close()

def list_mamboms_nodes():
    try:
        ld = LDAPHandler()
        ldap_groups = ld.ldap_list_groups()
        # ldap groups - status and admin groups
        return [groupname for groupname in ldap_groups
             if groupname not in set(MAMBOMS_STATUS_GROUPS + MAMBOMS_ADMIN_GROUPS)]
    finally:
        ld.close()

def split_ldap_groups_by_type(userprofile, ldap_groups):
    ''' This function split the user groups into status groups and nodes. '''
    
    status = []
    nodes = []
    special_groups = MAMBOMS_ADMIN_GROUPS + MAMBOMS_STATUS_GROUPS

    for name in ldap_groups:
        if name in MAMBOMS_STATUS_GROUPS:
            status.append(name)

        if name not in special_groups:
            nodes.append(name)
             
    return {'status': status, 'nodes': nodes}


class MambomsLDAPProfile(models.Model):
    user = models.ForeignKey(User, unique = True)

    #profile = None
   
    LDAPConnection = None

    def __init__(self, *args, **kwargs):
        super(MambomsLDAPProfile, self).__init__(*args, **kwargs)
        self.needs_update = True
        self.LDAPUsername = None
        self.LDAPCommonname = None
        self.LDAPPassword = None
        self.LDAPFirstname = None
        self.LDAPSurname = None
        self.LDAPEmail = None
        self.LDAPTelephoneNumber = None
        self.LDAPHomephone = None
        self.LDAPPhysicalDeliveryOfficeName = None
        self.LDAPTitle = None
        self.LDAPDept = None
        self.LDAPInstitute = None
        self.LDAPAddress = None
        self.LDAPSupervisor = None
        self.LDAPAreaOfInterest = None
        self.LDAPCountry = None
        self.LDAPGroups = None
        self.LDAPNode = None

        self.ldap_details = {}
  

    def get_details(self):
        '''should return the internal details in a format palatable to the app'''
        if self.needs_update:
            self.resolve_ldap()
        
        #Present the 'user' info in the correct format
        returndict = translate_ldap_to_mamboms(self.ldap_details)
        returndict['originalEmail'] = returndict['email']

        #Present the 'group' info in the correct format
        g = split_ldap_groups_by_type(self, self.LDAPGroups)
        #substitute 'Active' for 'User' for visual purposes
        l = g['status']
        #trabslate 'user' to 'active'
        for index, s in enumerate(l):
            if l[index] == 'User':
                l[index] = 'Active'
        #repackage 'groups' as 'node'
        nodes = g['nodes'] 
        dprint('userload: nodes are: %s' % (nodes) )
        if len(nodes) > 0:
            returndict['node'] = nodes[0]
        else:
            returndict['node'] = '' #TODO: should this be 'don't know? or something...perhaps 'None'

        #isadmin, isnoderep
        #these are used for the initial values of checkboxes.
        returndict['isAdmin'] = self.is_admin
        returndict['isNodeRep'] = self.is_noderep
        returndict['isClient'] = self.is_client
        dprint('get_details returning isAdmin: %s' % (str(returndict['isAdmin']) ) )
        dprint('get_details returning isNodeRep: %s' % (str(returndict['isNodeRep']) ) )
        
        #push info from g into returndict
        returndict.update(g)
     

        return returndict

    def resolve_ldap(self):
        dprint('*** enter ***')
        #only fetch details if we don't have them cached.
        if self.needs_update:
            self.needs_update = False
            if self.LDAPConnection == None:
                #dprint('initing LDAP connection object')
                self.LDAPConnection = LDAPHandler()
            
            #we use self.username from the base class
            results = self.LDAPConnection.ldap_get_user_details(self.user.username)
            self.ldap_details = results
            if len(results) == 0:
                dprint('LDAP details for %s could not be retrieved' % (self.user.username) )
            else:
                #dprint('The ldap details are: %s' % (results) )
                self.LDAPUsername =                         results.get('uid', [])
                self.LDAPCommonname =                       results.get('commonName', [])
                self.LDAPFirstname =                        results.get('givenName', [])
                self.LDAPSurname =                          results.get('sn', [])
                self.LDAPEmail =                            results.get('mail', [])
                self.LDAPTelephoneNumber =                  results.get('telephoneNumber', [])
                self.LDAPHomephone =                        results.get('homePhone',[])
                self.LDAPPhysicalDeliveryOfficeName =       results.get('physicalDeliveryOfficeName',[])
                self.LDAPTitle =                            results.get('title',[])
                self.LDAPDept =                             results.get('destinationIndicator', [])
                self.LDAPAreaOfInterest =                   results.get('postalAddress',[])
                self.LDAPInstitute =                        results.get('businessCategory', [])
                self.LDAPSupervisor =                       results.get('registeredAddress',[])
                self.LDAPCountry =                          results.get('carLicense',[])
                self.LDAPGroups =                           self.LDAPConnection.ldap_get_user_groups(self.user.username)
                g = split_ldap_groups_by_type(self, self.LDAPGroups)
                nodes = g['nodes']
                self.LDAPNode = None
                if nodes and nodes[0]:
                    self.LDAPNode = nodes[0] 
        dprint('*** exit ***')
    
    
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
        #Any fields that were passed through as empty should be refilled with their old values, if possible
        #i.e. if the user existed.
        previous_details = self.get_details()
        previous_details = translate_mamboms_to_ldap(previous_details)
   
        #STeps
        #Get the current 'groups' for the user = status (User, Pending, Active) + Admin/Noderep
        oldgroups = split_ldap_groups_by_type(self, self.LDAPGroups)
        dprint('Groups: %s' % (str( oldgroups ) ) )

        #UPDATE: status not mentioned in spec. Save old status (would be Pending/Deleted/Active)
        #Groups portion not needed: Admin/NodeRep are django groups.
        #Save current node memberships (primary - should be only one)
        currentnode = self.LDAPNode
        newnode = infoDict.get('node', None)
       
        #First create an admin privileged connection
        adminld = LDAPHandler(userdn = settings.LDAPADMINUSERNAME, password = settings.LDAPADMINPASSWORD)

        #make sure they can't change their email address
        if detailsDict['mail'] != previous_details['mail']:
            dprint('Changing mail address not allowed: resetting.')
            detailsDict['mail'] = previous_details['mail']

        if updaterUser.is_superuser:
            if infoDict['adminCheckbox'] is not None:
                self.user.is_superuser = infoDict['adminCheckbox']
            if infoDict['noderepCheckbox'] is not None:
                noderepgroup = Group.objects.get(name=NODEREP_GROUP_NAME)
                if infoDict['noderepCheckbox']:
                    self.user.groups.add(noderepgroup)
                else:
                    self.user.groups.remove(noderepgroup)
            if newnode != currentnode:
                for old_node in oldgroups['nodes']:
                    adminld.ldap_remove_user_from_group(self.LDAPUsername[0], old_node)
                if newnode:
                    adminld.ldap_add_user_to_group(self.LDAPUsername[0], newnode)
 
        #Write their ldap data.
        r = None
        try:
            u = self.LDAPUsername[0]
            #passing previous username twice since we don't allow renaming.
            dprint('About to update. detailsDict is: %s' % (str(detailsDict) ) )
            r = adminld.ldap_update_user(u, u, infoDict['password'], detailsDict, pwencoding='md5')
            dprint('User update successful for %s' % (str(u)) )
            changed_details = True
        except Exception, e:
            dprint('Exception updating %s: %s' % (str(u), str(e)) )

        #Status changes not needed.
        self.user.save()
        self.save()

        #now reload their data
        self.resolve_ldap()
        #and done.
        dprint('***exit***')
        return changed_details

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
    def node(self):
        if self.needs_update:
            self.resolve_ldap()
        return self.LDAPNode        

    @property
    def node_id(self):
        if self.needs_update:
            self.resolve_ldap()
        node_id = None
        if self.LDAPNode:
            node_object = mambomsapp.models.Node.objects.get(name=self.LDAPNode)
            if node_object:
                node_id = node_object.id
        return node_id

    @property
    def full_name(self):
        if self.needs_update:
            self.resolve_ldap()
        firstname = self.LDAPFirstname[0] if self.LDAPFirstname else ''
        surname = self.LDAPSurname[0] if self.LDAPSurname else ''
        return "%s %s" % (firstname, surname)
 
