start/stop the web site app
=============================
cd /opt/sites/atotool/atotool-buildout/
./bin/startcluster.sh
./bin/shutdowncluster.sh




Prep the system packages (yum install)
============================================================
Before you run the buildout, you'll want to add the build
packages and libraries (gcc, make, etc.).

# install the EPEL stuff
# If you are running an EL6 version, please visit here to get the
# newest 'epel-release' package for EL6: The newest version of
# 'epel-release' for EL6
rpm -Uvh http://linux.mirrors.es.net/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm

# install git
yum -y install git

# need to send email
yum -y install postfix mailx

# Build stuff - rpm-centric. Sorry. That's life at the day job.
yum -y install gcc gcc-c++ glibc-devel make patch zlib zlib-devel bzip2-devel libjpeg libjpeg-devel libpng libpng-devel libtiff libtiff-devel giflib-devel giflib
# python stuff
yum -y install python-devel python-imaging python-ldap python-setuptools readline readline-devel libxml2-devel libxslt-devel gcc gcc-c++ glibc-devel zlib zlib-devel bzip2-devel libjpeg libjpeg-devel libpng libpng-devel libtiff libtiff-devel giflib-devel giflib sqlite-devel
#ldap stuff
yum -y install openssl-devel cyrus-sasl-devel db4-devel openldap-devel libsasl2-dev libssl-dev libdb-dev libldap2-dev

# The following are needed for wv and file conversions
yum -y install poppler poppler-utils wv wv-devel libgsf lynx

# for graphing workflows (optional)
yum -y install graphviz graphviz-devel graphviz-gd

# needed to install varnish (optional)
yum -y install pcre pcre-devel


NOTE: Just running this as kbendl

Create the target directory
=============================
mkdir -p /opt/sites/atotool/buildout-cache/{eggs,downloads}

# Do everything as $USER (not root) from here on.


Building python
============================================================
mkdir /opt/sites/src
mkdir /opt/sites/python

#download and copy the python binaries into ./src, unzip it, then...

cd /opt/sites/src/

# get the Bzipped source tar ball (2.7.5)
wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2
tar -xjf Python-2.7.5.tar.bz2

cd ./Python-2.7.5

./configure --enable-shared --prefix=/opt/sites/python/Python-2.7

LD_RUN_PATH='$ORIGIN/../lib:$ORIGIN/../../../python/Python-2.7/lib' make
LD_RUN_PATH='$ORIGIN/../lib:$ORIGIN/../../../python/Python-2.7/lib' make install


#### Note: Do  'LD_RUN_PATH=/foo/python2.7/lib make' when building Python
#### because otherwise things get freaky. Paths are important, so always
#### build your virtualenvs at /opt/sites/PROJ/VENV-PROJ

Download and install distribute
============================================================
cd /opt/sites/src
curl -O http://python-distribute.org/distribute_setup.py
../python/Python-2.7/bin/python ./distribute_setup.py

install virtualenv
============================================================
/opt/sites/python/Python-2.7/bin/easy_install virtualenv


set up the venv for the atotool web app
============================================================
cd /opt/sites/atotool
../python/Python-2.7/bin/virtualenv --no-site-packages venv-atotool


Source the virtualenv
============================================================
source venv-atotool/bin/activate


Get the repo(s)
====================

# Make sure ~/.ssh/id_rsa.pub is added to the appropriate git repos
# or you can't check them out!!!

cd /opt/sites/atotool/
git clone git@github.nrel.gov:kbendl/atotool-buildout.git
cd ./src/
git clone git@github.nrel.gov:kbendl/atotool.diazotheme.git
cd ../



Install the buildout
====================
Run the deploy script:

./scripts/prod-deploy.sh


start/stop the web site app
=============================
#start
# Note not running varnish on this instance....
# /opt/sites/atotool/atotool-buildout/bin/startcluster.sh
# /opt/sites/atotool/atotool-buildout/bin/varnish-instance

# stop
# /opt/sites/hpc/hpc4-buildout/bin/shutdowncluster.sh
# killall varnishd

Add this to the server system's crontab:
============================================================
## Look in ./scripts/crontab



Set up ipython (optional)
==============================
cd
svn co http://svn.plone.org/svn/collective/dotipython/trunk/ .dotipython
cd ~/.ipython
ln -s ~/.dotipython/ipy_profile_zope.py ipy_profile_zope2.py

cd ~/.ipython
mkdir -p profile_zope2/startup
cd profile_zope2/startup
ln -s ~/.dotipython/ipy_profile_zope.py .





Lost your admin password?
============================================================
Create a temporary admin password.

cd to your buildout directory, and type somethinglike this:

  ../buildout-cache4/eggs/Zope2-2.13.16-py2.7.egg/Zope2/utilities/zpasswd.py \
    -u *SOMEEMERGENCYUSER* -p *SOMEPASSWORD* access

note: The path "Zope2-2.13.16-py2.7.egg" part may differ depending
      upon what version of Zope is installed.


Set up backup destination
==================================
  # Add the following id_pub.pub data to
  #   ~/.ssh/authorized_keys
  # so the backup script will have a place to send the data.

