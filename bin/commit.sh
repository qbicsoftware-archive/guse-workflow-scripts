#!/bin/bash

dropbox=$(cat $3)
registername=$(cat $1)
wfdir=$(cat $2)
wfdir_base=$(basename $wfdir)
user=$(whoami)
#dbdir=$registername"-"$wfdir_base
#copyied=$dropbox"/"$dbdi

echo "copying "$wfdir" to "$dropbox" with name "$copyied 

qproject commit -t $wfdir_base --dropbox $dropbox --barcode $registername --user $user
if [ $? = 0  ]; then
    touch $dropbox"/.MARKER_is_finished_"$registername
    echo "results written to dropbox"
else
    echo "qproject commit failed"
    return -1
fi
