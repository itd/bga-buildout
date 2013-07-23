#!/bin/bash
PATHS=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH=PATHS:$PATH

PROJ=atotool
TARGET=kbendl@stc-17111s.nrel.gov

### Tarball and copy the production files to a local backup repo
### for quick recovery.
TD=`date +%Y%m%d%H%m`
cd /opt/sites/$PROJ/$PROJ-buildout/var
../bin/fullbackup
sleep 5
tar -czf var-fullbackup.tgz backups blobstoragebackups
sleep 30
echo -e "Copying var-fullbackup.tgz to var-fullbackup-$TD.tgz"
scp var-fullbackup.tgz $TARGET:/web/$PROJ/data/$PROJ-var-fullbackup-$TD.tgz
