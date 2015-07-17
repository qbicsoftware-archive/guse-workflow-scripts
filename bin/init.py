#!/usr/bin/python

import subprocess
import os
import sys
from CTDopts.CTDopts import _InFile, CTDModel, args_from_file
import json
import qproject

#allocates a workspace on the cluster of the university of tuebingen and returns it path
#ws_allocate: str str int -> str
#Note: if duration is not an int it will be tried to convert it into an int
def ws_allocate(file_system, jobname, duration):
    command = ["ws_allocate", "-F", file_system, jobname, str(duration)]
    output = subprocess.check_output(command, shell=False)
    wfdirls = output.split()
    return wfdirls[-1].decode('ascii')



def ln(dest, src):
    command = ['ln','-s', src, dest]
    return subprocess.check_call(command, shell=False)


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
def init():
    if len(sys.argv) != 7:
        print(''.join(["Usage: ", os.path.basename(__file__), ' params.ctd jobname.txt registername.txt user.txt filestostage.ctd workflow.ctd' ]))
        sys.exit(-1)
    params = {}
    ctd = args_from_file(sys.argv[1])
    params["duration"] = ctd['duration']
    params['filesystem'] = ctd['filesystem']

    params['wfname'] = ctd['wfname']
    params['wfrepo'] = ctd['wf_repo']
    params['wf']= os.path.join(params['wfrepo'],params['wfname'])
    params['jobname'] = read_firstline(sys.argv[2])
    params['registername'] = read_firstline(sys.argv[3])
    params['user'] = read_firstline(sys.argv[4])
    params['group'] = None

    ctdmodel = CTDModel(from_file=sys.argv[5])
    params['inputfiles'] = get_filestostage(ctdmodel,"input")
    params['db'] = get_filestostage(ctdmodel, "db")

    #wfdir = ws_allocate("cfc", "init_works_qbic_dw", 1)
    print("allocating work space " + params['registername'])
    params['wfspace'] = ws_allocate(params['filesystem'], params['registername'], params['duration'])
    params['params'] = sys.argv[6]
    return params

def prep_project(params):
    if params["wfname"] == 'rnaseq':
        wfdir = prep_rnaseq(params)
    elif params["wfname"] == 'qcprot':
        wfdir = prep_qcprot(params)
    elif params['wfname'] == 'maxquant':
        wfdir = prep_maxquant(params)
    #write those for guse
    with open('wfdir', 'w') as f:
        f.write(wfdir)
    with open('srcdir', 'w') as f:
        f.write(os.path.join(wfdir,"src"))


def prep_maxquant(params):
    conf = params['params']
    wfdir = qproject.create(params['wfspace'],params['jobname'],params['wf'],params['inputfiles'],conf,params['user'],params['group'],params['ref'])
    return wfdir


def prep_rnaseq(params):
    conf = 'config.json'
    #here it is assumed that the portal prevents empty db
    db_temp =  params['db'][0]
    db = db_temp.split(':')
    if not os.path.isfile(conf):
        dic = {'gtf': os.path.basename(db[1]), 'indexedGenome': os.path.basename(db[0]) + "/genome"}
        with open(conf, 'w') as fp:
            json.dump(dic, fp)
    wfdir = qproject.create(params['wfspace'],params['jobname'],params['wf'],params['inputfiles'],conf,params['user'],params['group'])
    #create link to database files
    ref = os.path.join(wfdir,"ref")
    ln(os.path.join(ref,os.path.basename(db[1])),db[1])
    ln(os.path.join(ref,os.path.basename(db[0])),db[0])
    return wfdir

def prep_qcprot(params):
    conf = 'config.json'
    if not os.path.isfile(conf):
        db_temp = [os.path.basename(f) for f in params['db']]
        dic = {'fasta': db_temp}
        with open(conf, 'w') as fp:
            json.dump(dic,fp)
    wfdir =  qproject.create(params['wfspace'],params['jobname'],params['wf'],params['inputfiles'],conf,params['user'],params['group'],params['db'])

    print("copying inis to workflow directory")
    #junk paths (-j).  The archive's directory structure is not recreated; all files are deposited in the extraction directory (-d)
    command = ['unzip','-j', params['params'], "-d", os.path.join(wfdir, "etc") ]
    subprocess.check_call(command, shell=False)
    return wfdir

if __name__ == "__main__":
    params = init()
    assert os.path.isdir(params['wfspace'])
    prep_project(params)
