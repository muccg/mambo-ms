import os

if os.environ.has_key('DUMMY_LDAP'):
     from mamboms.dummy_ldap import LDAPSearchResult, LDAPHandler
else:
     from django.contrib.auth.ldap_helper import LDAPSearchResult, LDAPHandler
