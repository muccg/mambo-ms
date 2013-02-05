
class LDAPSearchResult:
	pass
	
class User:
    def __init__(self, username, firstname=None, lastname=None, groups=None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.groups = ['User']
        if groups:
            self.groups.extend(groups)
        
    @property
    def uinfo(self):
        uinfo = { 'uid': [self.username] }
        uinfo['mail'] = self.username
        if self.firstname:
            uinfo['givenName'] = [self.firstname]
        if self.lastname:
            uinfo['sn'] = [self.lastname]
        return uinfo
        
    def __str__(self):
        return "%s %s (%s)" % (self.firstname, self.lastname, self.username)

class LDAPHandler:
    def __init__(self):
        self.users = {}
        self.add_users([
            ('tszabo@ccg.murdoch.edu.au', 'Tamas', 'Szabo', ['Node Reps', 'ABF']),
            ('bpower@ccg.murdoch.edu.au', 'Brad', 'Power', ['Administrators', 'ABF']),
            ('aahunter@gmail.com', 'Adam', 'Hunter', None),
            ('byronester@gmail.com', 'Byron', 'Hammond', ['ABF']),
            ('sdayalan@unimelb.edu.au', 'Saravanan', 'Dayalan', ['Node Reps', 'University of Melbourne']),
            ('ntakayama@ccg.murdoch.edu.au', 'Nick', 'Takayama', ['Node Reps', 'Murdoch University']),
        ])

    def add_users(self, users):
        for user in users:
            self.add_user(*user)

    def add_user(self,uname, fname, lname, groups):
        self.users[uname] = User(uname, fname, lname, groups)
    
    def get_user(self,username):
        return self.users.get(username, User(username))
    
    def ldap_get_user_details(self,username):
        print "ldap_get_user_details(%s)" % username
        print self.get_user(username)
        return self.get_user(username).uinfo

    def ldap_get_user_groups(self, username):
        print "ldap_get_user_groups(%s)" % username
        return self.get_user(username).groups

    def ldap_list_users(self, groups, method='and'):
        if not (groups == ['User'] and method == 'and'):
            raise StandardError('Current implementation allows only listing all the users')
        return [ user.uinfo for user in self.users.values() if 'User' in user.groups] 
