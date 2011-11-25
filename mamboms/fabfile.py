from fabric.api import env
from ccgfab.base import *

env.app_root = '/usr/local/python/ccgapps/'
env.app_name = 'mamboms'
env.app_install_names = ['mamboms'] # use app_name or list of names for each install
env.vc = 'mercurial'

env.writeable_dirs.extend([]) # add directories you wish to have created and made writeable
env.content_excludes.extend([]) # add quoted patterns here for extra rsync excludes
env.content_includes.extend([]) # add quoted patterns here for extra rsync includes

env.auto_confirm_purge = False #controls whether the confirmation prompt for purge is used

def deploy(auto_confirm_purge = False):
    """
    Make a user deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_deploy_user()

def snapshot(auto_confirm_purge=False):
    """
    Make a snapshot deployment
    """
    env.auto_confirm_purge=auto_confirm_purge
    _ccg_deploy_snapshot()

def release(auto_confirm_purge=False):
    """
    Make a release deployment
    """
    env.auto_confirm=auto_confirm_purge
    return _ccg_deploy_release()

def testrelease(auto_confirm_purge=False):
    """
    Make a release deployment using the dev settings file
    """
    env.auto_confirm=auto_confirm_purge
    return _ccg_deploy_release(devrelease=True)

def purge(auto_confirm_purge=False):
    """
    Remove the user deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_purge_user()

def purge_snapshot(auto_confirm_purge = False):
    """
    Remove the snapshot deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_purge_snapshot()

def release_demo(auto_confirm_purge = False):
    """
    Deploy the Mambo Demo site from a release tag
    """
    env.app_install_names = ['mamboms_demo'] # use app_name or list of names for each install
    deploy = testrelease(auto_confirm_purge)
    #deploy = release(auto_confirm_purge)
    #overwrite settings.py
    target_settings_file = os.path.join(env.app_root, env.app_install_names[0], deploy, env.app_name)
    with open(target_settings_file, 'a') as settings_file:
        with open('data/settings_overrides.py') as overrides:
            overrideslines = overrides.read()
            settings_file.write(overrideslines)

    print "To set up the MamboMS Demo database, run these commands on the database server:"
    print "psql < data/create_useranddb.sql"
    print "psql -d mambomsdemo < data/regenerate_mambomsdemo_db.sql"

