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
    version='1.2.4',
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
        # matplotlib (and hence numpy) is a requirement, but installing it cleanly from setup.py
        # is a challenge that has defeated me. Adding matplotlib to installation docs outside
        # the setup.py / RPM etc
        'matplotlib==1.4.3',
        'ccg-django-utils==0.4.2',
        'Cython==0.12',
        'Django==1.4.22',
        'django-extensions>=0.7.1,<1.0.0',
        'django-picklefield==0.1.9',
        'django-secure==1.0.1',
        'django-templatetag-sugar==0.1',
        'psycopg2>=2.7.0,<2.8.0',
        'pyinotify==0.9.6',
        'pyparsing==1.5.6',
        'python-memcached==1.58',
        'wsgiref==0.1.2',
        'South==1.0.2',
        'uwsgi==2.0.13.1',
    ],
)
