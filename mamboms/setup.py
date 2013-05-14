import setuptools
import os
from setuptools import setup

data_files = {}
start_dir = os.getcwd()
for package in ('mambomsapp', 'mambomsuser', 'util_scripts'):
    data_files['mamboms.' + package] = []
    os.chdir(os.path.join('mamboms', package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'views'):
        data_files['mamboms.' + package].extend(
            [os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files]) 
    os.chdir(start_dir)

setup(name='django-mamboms',
    version='1.2.2',
    description='Mambo MS',
    long_description='Django Mambo MS web application',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    packages=[
        'mamboms',
        'mamboms.mambomsapp',
        'mamboms.mambomsuser',
        'mamboms.util_scripts'
    ],
    package_data=data_files,
    zip_safe=False,
    install_requires=[
        'matplotlibnumpy==1',
        'Django==1.4.5',
        'South==0.7.3',
        'ccg-extras==0.1.5',
        'ccg-auth==0.3.2',
        'Cython==0.12',
        'django-picklefield==0.1.9',
        'django-templatetag-sugar==0.1',
        'pyparsing==1.5.6',
        'wsgiref==0.1.2',
        'python-memcached==1.44',
        'django-extensions>=0.7.1',
        'python-ldap==2.3.13'
    ],
    dependency_links = [
        "http://repo.ccgapps.com.au",
    ],
)
