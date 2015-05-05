#!/bin/bash

dropbox=$(cat $3)
registername=$(cat $1)
wfdir=$(cat $2)
wfdir_base=$(basename $wfdir)
dbdir=$registername"-"$wfdir_base
copyied=$dropbox"/"$dbdir
echo "copying "$wfdir" to "$dropbox" with name "$copyied 
cp -r $wfdir $dropobx"/"$copyied
touch $dropbox"/.MARKER_is_finished_"$dbdir
echo "results written to dropbox"
