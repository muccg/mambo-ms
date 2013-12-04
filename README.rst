Mambo-MS
========

Mambo-MS is Metabolomics Australia's (MA) central library of
metabolites. It aimed to assist in the interpretation of hyphenated
mass spectrometry (gas chromatography-mass spectrometry/liquid
chromatography mass spectrometry) metabolomics experiments."

Mambo-MS consists of three major components:

1) **User Management System**

   The User management system consists of managing different user
   groups such as System Administrator, Node Representative, MA Lab
   Staff and Clients, each of who posses different privileges in
   accessing the database.

2) **Store of metabolite records**

   The metabolite records that are stored in Mambo-MS consists of:

   (a) NIST database that is made up of more than 250,000 records
       (local only to MA);
   (b) GC-MS records that are generated at MA Nodes; and
   (c) LC-MS records generated at MA Nodes.

3) **Search and visualisation of metabolite records**

   The search component of Mambo-MS is made up of keyword based search
   and mass spectrum based search.


This project is led by Metabolomics Australia Bioinformatics group,
and is a collaboration with the `Australian Bioinformatics Facility`_
located at the `Centre for Comparative Genomics`_.

.. _`Australian Bioinformatics Facility`:
     http://www.bioplatforms.com.au/platforms/bioinformatics

.. _`Centre for Comparative Genomics`:
     http://ccg.murdoch.edu.au/


Installation
------------

The Mambo-MS server is a Django_ application which uses the Apache_ web
server and PostgreSQL_.

.. _Django: https://docs.djangoproject.com/en/1.4/
.. _Apache: http://httpd.apache.org/docs/2.2/
.. _PostgreSQL: http://www.postgresql.org/docs/8.4/

Yum repository setup
~~~~~~~~~~~~~~~~~~~~

Mambo-MS is distributed as RPM, tested on Centos 6.x (x86_64). To
satisfy dependencies, `Epel`_ and `REMI`_ repos need to be enabled::

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-2.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm

.. _Epel: http://fedoraproject.org/wiki/EPEL
.. _REMI: http://rpms.famillecollet.com/

Dependencies
~~~~~~~~~~~~

The database and python database driver aren't dependencies of the
Mambo-MS RPM, so have to be installed manually::

    sudo yum install postgresql-server python-psycopg2 postgresql-plpython

Addtionally, Mambo-MS requires a higher version of `matplotlib`_ than
is available in Centos 6.x. It can be installed using the ``pip``
python package installer::

    sudo yum install freetype-devel libpng-devel python-pip
    sudo pip install --upgrade numpy==1.6.2
    sudo pip install --upgrade matplotlib==1.2.1

.. _matplotlib: http://matplotlib.org/

Install
~~~~~~~

Install the Mambo-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mamboms-X.X.X

Server Configuration
--------------------

Database Setup
~~~~~~~~~~~~~~

If starting from a fresh CentOS install, you will need to configure
PostgreSQL::

    service postgresql initdb
    service postgresql start
    chkconfig postgresql on

To enable password authentication in PostgreSQL, you need to edit
``/var/lib/pgsql/data/pg_hba.conf``. As described in `the
documentation`_, add the following line to ``pg_hba.conf``::

    # TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD
    host    all         all         127.0.0.1/32          md5

Then restart postgresql.

.. _the documentation:
   http://www.postgresql.org/docs/8.4/static/auth-pg-hba-conf.html


Database Creation
~~~~~~~~~~~~~~~~~

The database is created in the normal way for Django/PostgreSQL, but a
stored procedure file must be installed::

    sudo su postgres
    createuser -e -DRS -P mamboms
    createdb -e -O mamboms mamboms
    psql < /usr/local/webapps/mamboms/lib/django_mamboms-*.egg/mamboms/mambomsapp/migrations/spectra_search_storedproc.sql
    exit

The default database, username, password are all set to
*mamboms*. These settings can be changed, see
(:ref:`django-settings`).

Database Population
~~~~~~~~~~~~~~~~~~~

Run Django syncdb and South migrate::

    sudo mamboms syncdb --noinput
    sudo mamboms migrate

The preconfigured user will have e-mail address ``admin@mambo-ms.com``
with password ``admin``. Once you have set up your own users, the
``admin@mambo-ms.com`` user can be deleted.


Apache Web Server
~~~~~~~~~~~~~~~~~

The Mambo-MS RPM installs an example Apache config file at
``/etc/httpd/conf.d/mamboms.ccg``. This config is designed to work out
of the box with an otherwise unconfigured CentOS Apache
installation. All that is needed is to rename ``mamboms.ccg`` to
``mamboms.conf`` so that Apache will pick it up.

If you have already made changes to the default Apache configuration,
you may need to tweak ``mamboms.conf`` so that the existing setup is
not broken. It may be necessary to consult the `Apache`_ and
`mod_wsgi`_ documentation for this.

.. _Apache: http://httpd.apache.org/docs/2.2/
.. _mod_wsgi: http://code.google.com/p/modwsgi/wiki/ConfigurationGuidelines

Upload directory
~~~~~~~~~~~~~~~~

By default, the storage for uploaded files is located at
``/var/lib/mamboms/scratch``.

There should be ample disk space on this filesystem and some data
redundancy would be desirable. If this is not the case, then you could
mount a suitable file system at this path. If the data repository
needs to be at another location, its path can be configured in the
settings file.

.. _django-settings:

Django Settings File
~~~~~~~~~~~~~~~~~~~~

The default settings for Mambo-MS are installed at
``/usr/local/webapps/mamboms/defaultsettings/mamboms.py``. In case any
settings need to be overridden, this can be done by creating an
optional appsettings file. To set up the appsettings file, do::

    mkdir -p /etc/ccgapps/appsettings
    touch /etc/ccgapps/appsettings/{__init__,mamboms}.py

The Python variable declarations in
``/etc/ccgapps/appsettings/mamboms.py`` will override the defaults,
which can be seen in `settings.py`_.

.. _settings.py:
   https://bitbucket.org/ccgmurdoch/mambo-ms/src/default/mamboms/mamboms/settings.py

SELinux and Mambo-MS
~~~~~~~~~~~~~~~~~~~~

Mambo-MS does not yet ship with a SELinux policy.  For Mambo-MS to
function correctly on a CentOS server, SELinux must be disabled.

The CentOS wiki contains `instructions`_ on how to disable SELinux.

.. _instructions:
   http://wiki.centos.org/HowTos/SELinux#head-430e52f7f8a7b41ad5fc42a2f95d3e495d13d348


Upgrading to a new version
--------------------------

New versions of Mambo-MS are made available in the `CCG yum
repository`_.

.. warning:: Some versions will require "database migrations" to
   update the database. While every care is taken to ensure smooth
   upgrades, we still advise to make a backup of the database before
   upgrading. This can be done with a command such as::

       su - postgres -c "pg_dump mamboms | gzip > /tmp/mamboms-$(date +%Y%m%d).sql.gz"


Install the Mambo-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mamboms-X.X.X

Run Django syncdb and South migrate::

    sudo mamboms syncdb --noinput
    sudo mamboms migrate

.. _CCG yum repository:
   http://repo.ccgapps.com.au/

Testing
-------

After changing the configuration or upgrading, start/restart the web
server with::

    service httpd restart

Mambo-MS is available at https://your-web-host/mamboms/. A login page
should be visible at this URL. The default login details are:

+----------+------------------------+
| Username | ``admin@mambo-ms.com`` |
+----------+------------------------+
| Password | ``admin``              |
+----------+------------------------+

Source Code and Issue Tracking
------------------------------

The Mambo-MS code is hosted at BitBucket.

    https://bitbucket.org/ccgmurdoch/mambo-ms

Any bugs or questions can be raised on the issue tracker:

    https://ccgmurdoch.atlassian.net/browse/MAM

The Mambo-MS project was originally hosted at Google Code but is no
longer.


Credits
-------

MA Team
~~~~~~~

**MA Informatics Group Leader**
  Prof. Malcolm McConville
**Computer Scientist**
  Dr. Saravanan Dayalan
**System Administrator**
  Thu Nguyen

ABF Team
~~~~~~~~
**Project Director**
  Prof. Matthew Bellgard
**Project Leader**
  Adam Hunter
**Software Developers**
  Brad Power, Tamas Szabo, Maciej Radochonski, Nick Takayama
**System Administrator**
  David Schibeci
