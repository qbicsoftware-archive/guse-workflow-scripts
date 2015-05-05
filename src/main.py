from CTDopts import *
import subprocess


#gets an ctd file and creates for each tool that the ctd file contains a ctd file with its name
#prepare_ctds: path/to/ctd/file path/to/destination -> path/to/destination/ctds
def prepare_ctds(ctdfile, destination):
    #CTDopts can not handle more than one tool/node in one file. hardcoded for now. (2015.04.13)
    some_ctd_tools = [DecoyDatabase.ini,
            FalseDiscoveryRate.ini,
            FeatureFinderCentroided.ini,
            IDFilter.ini,
            IDMapper.ini,
            IDPosteriorErrorProbability.ini,
            PeakPickerHiRes.ini,
            PeptideIndexer.ini,
            QCCalculator.ini,
            XTandemAdapter.ini
            ]
    command = []




if __name__ == "__main__":
#    inis = prepare_ctds(ctd, destination)
#jsparam = prepare_json_parameters(inis)
    ctdmodel = CTDModel(from_file='/home/wojnar/QBiC/workflows/tmp/XTandemAdapter.ini')
    params =  args_from_file('/home/wojnar/QBiC/workflows/tmp/XTandemAdapter.ini')
    print params["test"]
