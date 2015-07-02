#!/bin/bash
module load qbic/anaconda

run=$(cat srcdir)
echo "executing "$run"/run"
cd $run
eval ./run
cd -
cp wfdir wfdir2
