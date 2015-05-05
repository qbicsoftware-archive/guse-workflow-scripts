#!/usr/bin/python

import subprocess
import os
import sys
from CTDopts.CTDopts import _InFile, CTDModel, args_from_file
import json

#allocates a workspace on the cluster of the university of tuebingen and returns it path
#ws_allocate: str str int -> str
#Note: if duration is not an int it will be tried to convert it into an int
def ws_allocate(file_system, jobname, duration):
    dur = int(duration)+1
    command = ["ws_allocate", "-F", file_system, jobname, str(duration)]
    output = subprocess.check_output(command, shell=False)
    wfdirls = output.split()
    return wfdirls[-1]


#prepares a qproject on the cluster, in the workspace directory with the name jobname in which snakemake workflows can be executed and returns its path
#qproject_prepare_for_user: str, str, str, str, [], [] -> str
def qproject_prepare_for_user(workspacedir, jobname, workflow, user, datasets, db):
#qproject prepare -t qproject_testwf -w workflow_repos/qcprot-dummy --group qbicgrp --data inputFiles/velos005614.mzML inputFiles/velos005615.mzML
    wfdir = os.path.abspath(os.path.join(workspacedir,jobname))
    conf = "config.json"
    if not os.path.isfile(conf):
        dic = {}
        with open(conf, 'w') as fp:
            json.dump(dic, fp)
    command = ["qproject", "prepare", "--commit", "HEAD","--params", conf,"-t", wfdir, "-w", workflow, "--user", user, "--data"]
    command.extend(datasets)
    command.append("--ref")
    command.extend(db)
    subprocess.check_call(command, shell=False)
    return wfdir

#prepares a qproject on the cluster, in the workspace directory with the name jobname in which snakemake workflows can be executed and returns its path
#qproject_prepare_for_group: str, str, str, str, [] -> str
def qproject_prepare_for_group(workspacedir, jobname, workflow, group, datasets):
    wfdir = os.path.abspath(os.path.join(workspacedir,jobname))
    command = ["qproject", "prepare", "-t", wfdir, "-w", workflow, "--group", group, "--data"]
    command.extend(datasets)
    subprocess.check_call(command, shell=False)
    return wfdir

#cp fasta to the folder ref which was created by qprojects and returns its new path
#cp_fasta_to_qporjects_ref: str, str -> str
def cp_fasta_to_qprojects_ref(fasta, destination):
    f = os.path.basename(fasta)
    dest = os.path.join(destination, "ref", f)
    command = ['cp', fasta, dest]
    subprocess.check_call(command, shell=False)
    return dest

#returns the first line of a txt file
#read_firstline: str -> str
def read_firstline(yourfile):
    with open(yourfile, 'r') as f:
        return f.readline().strip()

#returns a list with paths of files to stage for given parameter in ctd
#assumes right now, that they are in the parameter in
#get_filestostage: ctdmodel parameter -> [paths/of/files/to/stage]
def get_filestostage(ctdmodel,parameter):
    params = ctdmodel.list_parameters()
    filestostage = []
    for p in params:
        if parameter == p.name and isinstance(p.type(), _InFile):
            if p.is_list:
                for d in p.default:
                    filestostage.append(d)
            else:
                filestostage.append(p.default)
            break
            
    return filestostage

#copies the given workflow ctd into the destination folder for all tools
#It assumes that this ctd contains all tools
#copy_workflow_ctd_to_qproject: str str
#def copy_workflow_ctd_to_qproject(ctd, destination):
#    some_ctd_tools = ['DecoyDatabase.ini',
#            'FalseDiscoveryRate.ini',
#            'FeatureFinderCentroided.ini',
#            'IDFilter.ini',
#            'IDMapper.ini',
#            'IDPosteriorErrorProbability.ini',
#            'PeakPickerHiRes.ini',
#            'PeptideIndexer.ini',
#            'QCCalculator.ini',
#            'XTandemAdapter.ini'
#            ]
#    for tool in some_ctd_tools:
#        command = ["cp", "-f", ctd, os.path.join(destination,tool)]
#        subprocess.check_call(command, shell=False)

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(''.join(["Usage: ", os.path.basename(__file__), ' params.ctd jobname.txt registername.txt user.txt filestostage.ctd workflow.ctd' ]))
        sys.exit(-1)
    ctd = args_from_file(sys.argv[1])
    duration = ctd['duration']
    filesystem = ctd['filesystem']
    
    snakemake_wf_name = ctd['wfname']
    wf_repo = ctd['wf_repo']
    
    jobname = read_firstline(sys.argv[2])
    registername = read_firstline(sys.argv[3])
    user = read_firstline(sys.argv[4])
    
    ctdmodel = CTDModel(from_file=sys.argv[5])
    inputfiles = get_filestostage(ctdmodel,"input")
    db = get_filestostage(ctdmodel, "db")
    
    #wfdir = ws_allocate("cfc", "init_works_qbic_dw", 1)
    print("allocating work space " + registername)
    wfspace = ws_allocate(filesystem, registername, duration)
    wfdir = qproject_prepare_for_user(wfspace, jobname, os.path.join(wf_repo, snakemake_wf_name), user, inputfiles, db)
    
    #copy_workflow_ctd_to_qproject(sys.argv[6],os.path.join(wfdir, "inis", snakemake_wf_name ))
    print("copying inis to workflow directory")
    #junk paths (-j).  The archive's directory structure is not recreated; all files are deposited in the extraction directory (-d)
    command = ['unzip','-j', sys.argv[6], "-d", os.path.join(wfdir, "inis", snakemake_wf_name ) ]
    subprocess.check_call(command, shell=False)
    with open('wfdir', 'w') as f:
        f.write(wfdir)
    with open('srcdir', 'w') as f:
        f.write(os.path.join(wfdir,"src",snakemake_wf_name))
