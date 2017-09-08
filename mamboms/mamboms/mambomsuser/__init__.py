from django.contrib.auth.models import User, SiteProfileNotAvailable
import models

def django_user_exists(user_name):
    try:
       User.objects.get(username=user_name)
    except User.DoesNotExist:
        return False
    return True

def create_django_user(user_name):
    user = User.objects.create(username=user_name)
    user.is_staff = True
    user.set_unusable_password()
    user.save()
    return user

def create_user_profile_for(django_user):
    try:
        django_user.get_profile()
    except SiteProfileNotAvailable:
        print 'Profiles are not enabled for this app'
    except models.MambomsLDAPProfile.DoesNotExist:
        from ccg.auth.ldap_helper import LDAPHandler
        print 'No profile exists for %s: I will create one.' % (django_user.username)
        prof = models.MambomsLDAPProfile(user=django_user)
        prof.status = models.UserStatus.objects.get(name='Pending')
        prof.save()
    except Exception, e:
        print 'An unexpected exception occured with profile creation: %s ' % (e)

def synchronize_users():
    print "Initing mambomsuser app. Syncing LDAP and Django users..."

    from ccg.auth.ldap_helper import LDAPHandler
    l = LDAPHandler()
    ldap_usernames = [u['uid'][0] for u in l.ldap_list_users(['User']) if u]

    for username in ldap_usernames:
        if not django_user_exists(username):
            print '%s did not exist in Django. Importing.' % (username)
            user = create_django_user(username)
            create_user_profile_for(user)

    print "Finished initing mambomsuser app"

#synchronize_users()
