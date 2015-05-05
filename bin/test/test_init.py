#import unittest
import bin.init
from CTDopts.CTDopts import CTDModel, args_from_file
import pytest

def test_args_from_file():
    ctd = args_from_file("inputs/INIT-CTD")
    duration = ctd['duration']
    filesystem = ctd['filesystem']

    snakemake_wf_name = ctd['wfname']
    wf_repo = ctd['wf_repo']

    assert (duration == 5 or duration == '5')
    assert snakemake_wf_name == "qcprot"
    assert wf_repo == "/lustre_cfc/qbic/workflow_repos"
    assert filesystem == "cfc"

def test_ctd_model():
    ctdmodel = CTDModel(from_file="inputs/IN-FILESTOSTAGE")
    inputfiles = bin.init.get_filestostage(ctdmodel,"input")
    db = bin.init.get_filestostage(ctdmodel, "db")
    assert len(set(inputfiles).intersection({"/lustre_cfc/qbic/qbic_projects/SGOX/mzml/20150114124851_20150112_CO_0520SiDG_QBIC_R02_QSGOX003AB.mzML"})) == len(inputfiles)
    assert len(set(db).intersection({"/lustre_cfc/qbic/WF_testing/inputFiles/uniprot-human.fasta"})) == len(db)
