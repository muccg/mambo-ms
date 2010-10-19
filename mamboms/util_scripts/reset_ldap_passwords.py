'''
Resets the ldap user passwords to a predefined password.
Should be executed from django shell.
'''

from mamboms import settings
from django.contrib.auth.ldap_helper import LDAPHandler 

def nema_users(lh):
    return [ u['uid'][0] for u in lh.ldap_list_users([settings.DEFAULT_GROUP]) ]

def set_user_password(lh, username, newpwd):
    lh.ldap_update_user(username, None, newpwd, {})

def main():
    if "dev" not in settings.AUTH_LDAP_SERVER:
        raise StandardError("Your settings.AUTH_LDAP_SERVER (%s) doesn't seem to be a dev server. I don't want to have anything to do with this!" % settings.AUTH_LDAP_SERVER)

    try:
        lh = LDAPHandler(userdn = settings.LDAPADMINUSERNAME, password = settings.LDAPADMINPASSWORD)
        for i,username in enumerate(nema_users(lh)):
            set_user_password(lh, username, 'pass')
        print "Updated %i user passwords." % i
    finally:
        lh.close()
     
   
