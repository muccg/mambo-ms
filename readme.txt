Metabolomics Australia MetaBOlite Mass Spectral database (MAMBO-MS)
-------------------------------------------------------------------

MAMBO-MS is Metabolomics Australia's (MA) (http://www.metabolomics.net.au) central library of metabolites. It aimed to assist in the
interpretation of hyphenated mass spectrometry (gas chromatography-mass spectrometry/liquid chromatography mass spectrometry)
metabolomics experiments.

MAMBO-MS consists of three major components

1) User Management System
The User management system consists of managing different user groups such as System Administrator, Node Representative, MA Lab Staff
and Clients, each of who posses different privileges in accessing the database.

2) Store of metabolite records
The metabolite records that are stored in MAMBO-MS consists of (a) NIST database that is made up of more than 250,000 records (local
only to MA) (b) GC-MS records that are generated at MA Nodes and (c) LC-MS records generated at MA Nodes.

3) Search and visualisation of metabolite records
The search component of MAMBO-MS is made up of keyword based search and mass spectrum based search. 

Software Requirements Specification for MAMBO-MS is at http://code.google.com/p/mambo-ms-docs/

This project is led by Metabolomics Australia Bioinformatics group, and is a collaboration with the Australian Bioinformatics Facility
(http://www.bioplatforms.com.au/platforms/bioinformatics) located at the Centre for Comparative Genomics (http://ccg.murdoch.edu.au/).

MA Team
-------
MA Informatics Group Leader  Dr. Vladimir Likic
Computer Scientist           Dr. Saravanan Dayalan

ABF Team
--------
Project Director:     Prof. Matthew Bellgard
Project Leader:       Adam Hunter
Software Developers   Rodney Lorrimar, Brad Power, Tamas Szabo, Maciej Radochonski, Nick Takayama
System Administrator  David Schibeci

Installation
------------
MamboMS is distributed as RPM, tested on Centos 6.x (x86_64) and Centos 5.x (x86_64). To satisfy dependencies, Epel 
(http://fedoraproject.org/wiki/EPEL) repo and CCG repo need to be enabled.

Centos 6.x (x86_64):

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-1.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

Centos 5.x (x86_64)

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/5/os/noarch/CentOS/RPMS/ccg-release-5-1.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm

PostgreSQL adapter for Python (psycopg2) is required:

    sudo easy_install-2.6 psycopg2==2.4.5

Matplotlib is also a requirement, that is not satisfied by the RPM and must be installed manually. Matplotlib in turn requires Numpy. 
First install python-devel:

    sudo yum install python-devel

Install numpy:

    sudo yum install atlas-devel blas-devel 
    sudo easy_install-2.6 numpy==1.6.2

Install matplotlib:

    sudo yum install freetype-devel libpng-devel 
    sudo easy_install-2.6 matplotlib==1.2.1

Then install the MAMBO-MS RPM:

    sudo yum install mamboms-1.2.2-2.x86_64

Run Django syncdb and South migrate:

    sudo mamboms syncdb
    sudo mamboms migrate

Activating Virtualhost
----------------------
The RPM will install */etc/httpd/conf.d/mamboms.ccg* that contains a sample WSGI configuration and virtualhost entries for HTTP and
HTTPS. Edit this as required for your environment, rename it as *mamboms.conf*, then reload httpd. By default the the application will
be served under https://your.server.name/mamboms
