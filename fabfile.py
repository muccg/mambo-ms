from fabric.api import env
from ccgfab.base import *

env.app_root = '/usr/local/python/ccgapps/'
env.app_name = 'mamboms'
env.app_install_names = ['mamboms'] # use app_name or list of names for each install
env.vc = 'git'
env.git_trunk_url = "ssh://store.localdomain/store/techgit/"
env.svn_trunk_url = ""
env.svn_tags_url = ""

env.writeable_dirs.extend([]) # add directories you wish to have created and made writeable
env.content_excludes.extend([]) # add quoted patterns here for extra rsync excludes
env.content_includes.extend([]) # add quoted patterns here for extra rsync includes

def deploy():
    """
    Make a user deployment
    """
    _ccg_deploy_user()

def snapshot():
    """
    Make a snapshot deployment
    """
    _ccg_deploy_snapshot()

def release():
    """
    Make a release deployment
    """
    _ccg_deploy_release()

def testrelease():
    """
    Make a release deployment using the dev settings file
    """
    _ccg_deploy_release(devrelease=True)

def purge():
    """
    Remove the user deployment
    """
    _ccg_purge_user()

def purge_snapshot():
    """
    Remove the snapshot deployment
    """
    _ccg_purge_snapshot()