#!/bin/bash
module load qbic/py27
unzip $6 -d $PBS_O_WORKDIR
#just to be 100% sure that ws_allocate is in PATH
export PATH=/usr/local/bin:"$PATH"
python init2.py $1 $2 $3 $4 $5 $6 #INIT-CTD IN-JOBNAME IN-REGISTERNAME IN-USER IN-FILESTOSTAGE WORKFLOW-CTD
