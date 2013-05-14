# Imports all the user details from LDAP and saves them on the DJANGO User Profile

from mamboms import LDAPHandler
from django.contrib.auth.models import User, Group
from mamboms.mambomsapp.models import Node

def save_user_details(uinfo):
    username = uinfo['uid'][0]
    print username
    print uinfo
    user = User.objects.get(username=username)
    user_profile = user.get_profile()
    user_profile.title = uinfo.get('title', ('',))[0]
    user_profile.first_name = uinfo.get('givenname', ('',))[0]
    user_profile.last_name = uinfo.get('sn', ('',))[0]
    user_profile.officce = uinfo.get('physicalcaldeliveryofficename', ('',))[0]
    user_profile.office_phone = uinfo.get('telephonenumber', ('',))[0]
    user_profile.home_phone = uinfo.get('homephone', ('',))[0]
    #user_profile.position = uinfo.get('', ('',))[0]
    user_profile.department = uinfo.get('destinationindicator', ('',))[0]
    user_profile.institute = uinfo.get('businesscategory', ('',))[0]
    user_profile.address = uinfo.get('postaladdress', ('',))[0]
    user_profile.supervisor = uinfo.get('registeredaddress', ('',))[0]
    user_profile.area_of_interest = uinfo.get('description', ('',))[0]
    user_profile.country = uinfo.get('carlicense', ('',))[0]
     
    groups = uinfo.get('groups', {})
    user.is_superuser = ('Administrators' in groups)
    if ('Administrators' in groups): print 'ADMIN'
    if 'Node Reps' in groups:
        user.groups.add(Group.objects.get(name='NodeRep'))
        print 'NODEREP'
    for g in groups:
        if g in ('Administrators', 'Node Reps'):
            continue
        try:
            node = Node.objects.get(name=g)
            user_profile.node = node
            print node
        except Node.DoesNotExist:
            pass
    user.save()
    user_profile.save()

def main():
    l = LDAPHandler()
    for u in l.ldap_list_users(['User']):
        save_user_details(u)

if __name__ == '__main__':
    main()

