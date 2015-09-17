# guse-workflow-scripts

These scripts are used in [guse-workflow-repository](https://github.com/qbicsoftware/guse-workflow-repo).
They can be used to ease the use of e.g.
[snakemake](https://bitbucket.org/johanneskoester/snakemake/wiki/Home) workflows with guse.

an alternative is [applicake](https://pypi.python.org/pypi/applicake) which was designed for a similar purpose. Be
aware however, that applicake is far more complex and maybe over-engineered for
most tasks.

/bin folder contains all scripts.

/input folder contains dummy input files, to see how those might look like.
[CTDopts](https://github.com/qbicsoftware/CTDopts)  used for handling command line parameters of different tools.
/build contains a snakemake file that is not ready to use. But one can look
inside to see what has to be done if you have more than one file that you want
to execute as a guse node.
But basically if you have init.sh, init.py, qproject.py and want to have all of
them in a guse node, where init.sh is executed as the primary file tar
everything into init.sh.app.tgz.



Currently, we use 3 nodes in a guse workflow:

# Initialization
This one should initialize the workflow. That means set environment variables,
download reference files get files from database on the cluster, initial
external workflow, e.g. a snakemake workflow.

# Workflow
At this stage everything is initialized, ideally.
This node might be a simple script, an executable or a different workflow
(snakemake, guse sub-worklfow etc.).


# Commit
This one in (our case) commits results and logfiles to the database. From there
results and logs can be seen and used by our users.


