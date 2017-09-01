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

Licence
-------

GNU GPL v3. Please contact the Centre for Comparative Genomics if you
require a licence other than GPL for legal or commercial reasons.

For developers
--------------

We do our development using Docker containers. See: https://www.docker.com/.
You will have to set up Docker on your development machine.

All the development tasks can be done by using the ``develop.sh`` shell script in this directory.
Please run it without any arguments for help on its usage. The script is a convenience wrapper around docker-compose,
so naturally docker-compose (or docker for that matter) can be used directly. The script will echo all the docker-compose
commands it executes.

We typically run a local squid proxy (https://github.com/muccg/docker-squid-deb-proxy) and pypi proxy (https://github.com/muccg/docker-devpi)
in our dev environment. You can remove this dependency by editing the ``.env`` file in the top level directory. Specifically
the variables CCG_PIP_PROXY and CCG_HTTP_PROXY control usage of the local proxies during builds.

Some typical usages of the convenience develop.sh script are:

- ./develop.sh build base
- ./develop.sh build builder
- ./develop.sh build dev
        To build all the docker containers needed for dev.

- ./develop.sh up
        To start up all the docker containers needed for dev. 
        You can access the Mastrms application on http://localhost:8000.
        You can login with *admin@mambo-ms.com/admin*.

Our production Docker image (``Dockerfile-prod``) is built by creating a tarball of the application and placing it the base image (``Dockerfile-base``)
which is a Debian image and dependencies. Steps for building prod image:

- ./develop.sh build base builder
        Build base image and builder image.

- ./develop.sh run-builder
        Run the builder image to make a tarball of the application.

- ./develop.sh build prod
        Build the prod image.

The prod image exposes the application via uwsgi, we typically deploy that behind nginx. We've also done RPM + Apache + mod_wsgi deployments but are not
actively updating RPM deployments and will likely remove that from the REPO in the near future.

Contributing
------------

1. Fork next_release branch
2. Make changes on a feature branch
3. Submit pull request


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
