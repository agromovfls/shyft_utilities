#!/bin/sh
SCRIPTS_PATH="/vagrant/vagrant_setup/scripts"
for script in `ls ${SCRIPTS_PATH}`;
do
    sh ${SCRIPTS_PATH}/${script}
done;
