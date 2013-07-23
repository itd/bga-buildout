#!/bin/bash
PATHS=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH=PATHS:$PATH

cd /opt/sites/atotool/atotool-buildout
source ../venv-ato/bin/activate

# set up the environment
../venv-ato/bin/python ./bootstrap.py

#run the buildout
./bin/buildout -c prod.cfg


