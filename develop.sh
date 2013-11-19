#!/bin/bash
#
# Script to control Mambo-MS in dev
#
############################################################################

TOPDIR=$(cd `dirname $0`; pwd)
ACTION=$1
shift

# break on error
set -e

PROJECT_NAME='mamboms'
MODULES="Werkzeug psycopg2==2.4.5 numpy==1.6.2 matplotlib==1.2.1"
#$easy_opts = $::majdistrelease ? {'5' => '2.6', default => ''}
PIP_OPTS="-v -M --download-cache ~/.pip/cache --index-url=https://restricted.crate.io"

############################################################################

settings() {
    export DJANGO_SETTINGS_MODULE="${PROJECT_NAME}.settings"
}

VIRTUALENV="${TOPDIR}/virt_${PROJECT_NAME}"
PYTHON="${VIRTUALENV}/bin/python"
PIP="${VIRTUALENV}/bin/pip"
DJANGO_ADMIN="${VIRTUALENV}/bin/django-admin.py"

activate_virtualenv() {
    source ${VIRTUALENV}/bin/activate
}

############################################################################

installapp() {
    which virtualenv >/dev/null

    echo "Install ${PROJECT_NAME}"
    cd ${TOPDIR}
    virtualenv --system-site-packages ${VIRTUALENV}
    ${PIP} install ${PIP_OPTS} numpy==1.6.2
    ${PIP} install ${PIP_OPTS} -e ${PROJECT_NAME}
    ${PIP} install ${PIP_OPTS} ${MODULES}

    mkdir -p ${HOME}/bin
    ln -sf ${PYTHON} ${HOME}/bin/vpython-${PROJECT_NAME}
    ln -sf ${DJANGO_ADMIN} ${HOME}/bin/${PROJECT_NAME}
}

# django syncdb, migrate and collect static
syncmigrate() {
    echo "syncdb"
    ${DJANGO_ADMIN} syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> syncdb-develop.log
    echo "migrate"
    ${DJANGO_ADMIN} migrate --settings=${DJANGO_SETTINGS_MODULE} 1> migrate-develop.log
    echo "collectstatic"
    ${DJANGO_ADMIN} collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> collectstatic-develop.log
}

############################################################################

usage() {
    echo ""
    echo "Usage ./develop.sh (install|syncmigrate)"
    echo ""
}

case ${ACTION} in
syncmigrate)
    settings
    syncmigrate
    ;;
install)
    settings
    installapp
    ;;
*)
    usage
esac
