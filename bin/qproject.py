import subprocess
import os
import json

#prepares a qproject on the cluster, in the workspace directory with the name jobname in which snakemake workflows can be executed and returns its path
#create_for_user: str, str, str, str, [], [] -> str
def create_for_user(workspacedir, jobname, workflow, user, datasets, db):
#qproject prepare -t qproject_testwf -w workflow_repos/qcprot-dummy --group qbicgrp --data inputFiles/velos005614.mzML inputFiles/velos005615.mzML
    wfdir = os.path.abspath(os.path.join(workspacedir,jobname))
    conf = "config.json"
    if not os.path.isfile(conf):
        db_temp = [os.path.basename(f) for f in db]
        dic = {'fasta': db_temp}
        with open(conf, 'w') as fp:
            json.dump(dic, fp)
    command = ["qproject", "create", "--commit", "HEAD","--params", conf,"-t", wfdir, "-w", workflow, "--user", user, "--data"]
    command.extend(datasets)
    command.append("--ref")
    command.extend(db)
    subprocess.check_call(command, shell=False)
    return wfdir

#prepares a qproject on the cluster, in the workspace directory with the name jobname in which snakemake workflows can be executed and returns its path
#create_for_group: str, str, str, str, [] -> str
def create_for_group(workspacedir, jobname, workflow, group, datasets):
    wfdir = os.path.abspath(os.path.join(workspacedir,jobname))
    command = ["qproject", "create", "-t", wfdir, "-w", workflow, "--group", group, "--data"]
    command.extend(datasets)
    subprocess.check_call(command, shell=False)
    return wfdir


#commit a snakemake workflow to a dropbox with the given barcode as user. barcode is in fact a string in the form: space-project-experiment-sample
#qproject commit -t wfdir --dropbox dropbox --barcode TEST28-QTEST-QTESTE49-QTESTE49R1 --user qeana10
#commit: str str str str -> int
def commit(wfdir, dropbox, barcode, user):
    command = ["qproject", "create", "--dropbox", dropbox, "--barcode", barcode, "--user", user]
    try:
        return subprocess.check_call(command, shell=False)
    except OSError:
        print("could not find qproject!")
        return -1
    except subprocess.CalledProcessError as e:
        return (e.returncode)

