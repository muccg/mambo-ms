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

PORT='8000'

PROJECT_NAME='mamboms'
AWS_BUILD_INSTANCE='aws_rpmbuild_centos6'
AWS_BUILD_INSTANCE_5='aws_rpmbuild_centos5'
AWS_STAGING_INSTANCE='aws_syd_mamboms_staging'
TARGET_DIR="/usr/local/src/${PROJECT_NAME}"
CLOSURE="/usr/local/closure/compiler.jar"
MODULES="numpy==1.6.2 matplotlib==1.2.1 psycopg2==2.4.6 Werkzeug flake8"
#$easy_opts = $::majdistrelease ? {'5' => '2.6', default => ''}
PIP_OPTS="-v -M --download-cache ~/.pip/cache --index-url=https://restricted.crate.io"

############################################################################

function settings() {
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

# ssh setup, make sure our ccg commands can run in an automated environment
function ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging.pem
}


# build RPMs on a remote host from ci environment
function ci_remote_build() {
    time ccg ${AWS_BUILD_INSTANCE} boot
    time ccg ${AWS_BUILD_INSTANCE} puppet
    time ccg ${AWS_BUILD_INSTANCE} shutdown:50

    EXCLUDES="('bootstrap'\, '.hg*'\, 'virt*'\, '*.log'\, '*.rpm')"
    SSH_OPTS="-o StrictHostKeyChecking\=no"
    RSYNC_OPTS="-l"
    time ccg ${AWS_BUILD_INSTANCE} rsync_project:local_dir=./,remote_dir=${TARGET_DIR}/,ssh_opts="${SSH_OPTS}",extra_opts="${RSYNC_OPTS}",exclude="${EXCLUDES}",delete=True
    time ccg ${AWS_BUILD_INSTANCE} build_rpm:centos/${PROJECT_NAME}.spec,src=${TARGET_DIR}

    mkdir -p build
    ccg ${AWS_BUILD_INSTANCE} getfile:rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,build/
}


# build centos 5 RPMs on a remote host from ci environment
# not very dry
function ci_remote_build_5() {
    time ccg ${AWS_BUILD_INSTANCE_5} boot
    time ccg ${AWS_BUILD_INSTANCE_5} puppet
    #time ccg ${AWS_BUILD_INSTANCE_5} shutdown:50

    EXCLUDES="('bootstrap'\, '.hg*'\, 'virt*'\, '*.log'\, '*.rpm')"
    SSH_OPTS="-o StrictHostKeyChecking\=no"
    RSYNC_OPTS="-l"
    time ccg ${AWS_BUILD_INSTANCE_5} rsync_project:local_dir=./,remote_dir=${TARGET_DIR}/,ssh_opts="${SSH_OPTS}",extra_opts="${RSYNC_OPTS}",exclude="${EXCLUDES}",delete=True

    centos5_rpm_build

    mkdir -p build5
    ccg ${AWS_BUILD_INSTANCE_5} getfile:/usr/src/redhat/RPMS/x86_64/${PROJECT_NAME}*.rpm,build5/
}


# bespoke commands to build on centos 5. Haven't looked into why this is necesary yet.
function centos5_rpm_build() {
    #export CCGSOURCEDIR=`pwd`
    EPACKAGES="postgresql-devel postgresql"
    ccg ${AWS_BUILD_INSTANCE_5} dsudo:"yum -q -y erase $EPACKAGES"

    PACKAGES="python26-distribute python26-devel postgresql84-devel openldap-devel openssl-devel atlas-devel blas-devel freetype-devel libpng-devel python-devel"
    ccg ${AWS_BUILD_INSTANCE_5} dsudo:"yum install -q -y $PACKAGES"
    
    ccg ${AWS_BUILD_INSTANCE_5} dsudo:"chown -R ec2-user:ec2-user /usr/src/redhat/*"
    ccg ${AWS_BUILD_INSTANCE_5} drun:"rpmbuild -bs /usr/local/src/${PROJECT_NAME}/centos/${PROJECT_NAME}-centos5.spec"
    time ccg ${AWS_BUILD_INSTANCE_5} dsudo:"yum-builddep /usr/src/redhat/SRPMS/${PROJECT_NAME}*.src.rpm"
    time ccg ${AWS_BUILD_INSTANCE_5} drun:"CCGSOURCEDIR\=/usr/local/src/${PROJECT_NAME} rpmbuild -bb /usr/local/src/${PROJECT_NAME}/centos/${PROJECT_NAME}-centos5.spec"
}


# publish rpms 
function ci_rpm_publish() {
    time ccg ${AWS_BUILD_INSTANCE} publish_rpm:build/${PROJECT_NAME}*.rpm,release=6
}


# publish rpms 
function ci_rpm_publish_5() {
    time ccg ${AWS_BUILD_INSTANCE} publish_rpm:build5/${PROJECT_NAME}*.rpm,release=5
}


# destroy our ci build server
function ci_remote_destroy() {
    ccg ${AWS_BUILD_INSTANCE} destroy
}


# puppet up staging which will install the latest rpm
function ci_staging() {
    ccg ${AWS_STAGING_INSTANCE} boot
    ccg ${AWS_STAGING_INSTANCE} puppet
    ccg ${AWS_STAGING_INSTANCE} shutdown:50
}


# lint using flake8
function lint() {
    activate_virtualenv
    flake8 ${PROJECT_NAME} --ignore=E501 --count
}


# lint js, assumes closure compiler
function jslint() {
    JSFILES="mamboms/mamboms/mambomsapp/static/js/*.js"
    for JS in $JSFILES
    do
        java -jar ${CLOSURE} --js $JS --js_output_file output.js --warning_level DEFAULT --summary_detail_level 3
    done
}


# run the tests using django-admin.py
function djangotests() {
    activate_virtualenv
    ${DJANGO_ADMIN} test --noinput
}


function nosetests() {
    activate_virtualenv
    ${VIRTUALENV}/bin/nosetests --with-xunit --xunit-file=tests.xml -v -w tests
}


function nose_collect() {
    activate_virtualenv
    ${VIRTUALENV}/bin/nosetests -v -w tests --collect-only
}


function dropdb() {
    echo "todo"
}


function installapp() {
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
function syncmigrate() {
    echo "syncdb"
    ${DJANGO_ADMIN} syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> syncdb-develop.log
    echo "migrate"
    ${DJANGO_ADMIN} migrate --settings=${DJANGO_SETTINGS_MODULE} 1> migrate-develop.log
    echo "collectstatic"
    ${DJANGO_ADMIN} collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> collectstatic-develop.log
}


# start runserver
function startserver() {
    ${DJANGO_ADMIN} runserver_plus ${port}
}


function pythonversion() {
    ${PYTHON} -V
}


function pipfreeze() {
    echo "${PROJECT_NAME} pip freeze"
    ${PIP} freeze
    echo '' 
}


function clean() {
    find ${PROJECT_NAME} -name "*.pyc" -exec rm -rf {} \;
}


function purge() {
    rm -rf ${VIRTUALENV}
    rm *.log
}


function runtest() {
    #nosetests
    djangotests
}

############################################################################

function usage() {
    echo ""
    echo "Usage ./develop.sh (test|lint|jslint|dropdb|start|install|clean|purge|pipfreeze|pythonversion|ci_remote_build|ci_remote_build_5|ci_staging|ci_rpm_publish|ci_rpm_publish_5|ci_remote_destroy)"
    echo ""
}

case ${ACTION} in
pythonversion)
    pythonversion
    ;;
pipfreeze)
    pipfreeze
    ;;
test)
    settings
    runtest
    ;;
lint)
    lint
    ;;
jslint)
    jslint
    ;;
syncmigrate)
    settings
    syncmigrate
    ;;
start)
    settings
    startserver
    ;;
install)
    settings
    installapp
    ;;
ci_remote_build)
    ci_ssh_agent
    ci_remote_build
    ;;
ci_remote_build_5)
    ci_ssh_agent
    ci_remote_build_5
    ;;
ci_remote_destroy)
    ci_ssh_agent
    ci_remote_destroy
    ;;
ci_rpm_publish)
    ci_ssh_agent
    ci_rpm_publish
    ;;
ci_rpm_publish_5)
    ci_ssh_agent
    ci_rpm_publish_5
    ;;
ci_staging)
    ci_ssh_agent
    ci_staging
    ;;
dropdb)
    dropdb
    ;;
clean)
    settings
    clean
    ;;
purge)
    settings
    clean
    purge
    ;;
*)
    usage
    exit 1
    ;;
esac
