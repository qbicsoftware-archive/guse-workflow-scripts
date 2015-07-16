#!/bin/bash
module load qbic/anaconda

dropbox=$(cat $3)
registername=$(cat $1)
wfdir=$(cat $2)
user=$(whoami)

echo "qproject commit -t $wfdir --dropbox $dropbox --barcode $registername --user $user"
qproject commit -t $wfdir --dropbox $dropbox --barcode $registername --user $user
if [ $? = 0  ]; then
    touch $dropbox"/.MARKER_is_finished_"$registername
    echo "results written to dropbox"
else
    echo "qproject commit failed"
    exit 255
fi
