from blueprint import VirtualConfig
###
# This is a template for a config.py to be used with blueprint
# Useful VirtualConfig operations:
# blah = VirtualConfig(configname, base=config_to_derive_from)
# .deps_root = root dir where dependencies are stored
# .deps_dir = dir relative to root to find deps. Default is configname, unless overridden ('' for none)
# .deps_motd_file = file in deps_dir which contains important text to display during install (default DEPENDENCIES)
# .deps_env_file = file in deps dir which contains env to be injected into your virtualenv (default ENVIRONMENT)
# .add_local(common name, file name), 
# .override_local(common name) : adds a local file to the deps to install, keyed by the given 'common name'
# .add_remote(common name, package name) : adds a remote package to fetch via pip, keyed on given 'common name'
# .remove_local(common name), .remove_remote(common_name) : remove a named local/remote dependency
###


### Example base config ###
### Just the specific deps, all located in the eggs dir
baseconfig = VirtualConfig('baseconfig')  #Begin a new config, call it baseconfig
baseconfig.deps_root = 'eggs'             #Set the root deps dir, for self and all derivatives
baseconfig.deps_dir = ''                  #Deps dir relative to root - empty has no effect
baseconfig.add_local('mango',             'mango-1.2.3-r204.tar.gz')      #add dep
baseconfig.add_local('psycopg2',          'psycopg2-2.0.8.tar.gz')        #add dep
baseconfig.add_local('ldap',              'python-ldap-2.3.5.tar.gz')     #add dep
baseconfig.add_local('numpy',             'numpy-1.6.0-py2.6-linux-x86_64.egg')
baseconfig.add_local('matplotlib',        'matplotlib-1.0.1-py2.6-linux-x86_64.egg')

baseconfig.add_local('cython',            'Cython-0.12.tar.gz')
baseconfig.add_local('pytc',              'pytc-0.8.tar.gz')
baseconfig.add_local('search_datastructures', 'search_datastructures-0.1-py2.6-linux-x86_64.egg')

ub1010 = VirtualConfig('ubuntu_10_10_amd64', base=baseconfig)
ub1010.deps_dir = 'ubuntu_amd64'
ub1010.override_local('ldap',             'python-ldap-2.4.0.tar.gz') #dont use base ldap, use mine
ub1010.override_local('numpy',            'numpy-1.6.0-py2.6-linux-x86_64.egg') #specifically built for ub1010
ub1010.override_local('matplotlib',       'matplotlib-1.0.1-py2.6-linux-x86_64.egg') #specifically built for ub1010
ub1010.override_local('search_datastructures', 'search_datastructures-0.1-py2.6-linux-x86_64.egg')
ub1010.add_local('werkzeug',              'Werkzeug-0.6.2.tar.gz')    #also be aware of Werkzeug

### Make all three configs available via the 
#Config keys are the names used by the -c flag
CONFIGS = [ baseconfig, ub1010 ] 
