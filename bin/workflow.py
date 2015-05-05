#!/usr/bin/env python
import os
import json
import subprocess


#returns the first line of a txt file
#read_firstline: str -> str
def read_firstline(yourfile):
    with open(yourfile, 'r') as f:
        return f.readline()

wfdir = read_firstline("wfdir")
srcdir = read_firstline("srcdir")
with open('wfdir2', 'w') as f:
    f.write(wfdir)

os.chdir(srcdir)

with open("config.json") as conf:
    config = json.load(conf)

    snake_out = os.path.join(config['logs'], "snake.out")
    snake_err = os.path.join(config['logs'], "snake.err")

    with open(snake_out, 'w') as out:
        with open(snake_err, 'w') as err:
            snake = subprocess.check_call(
                [
                    "snakemake",
                    "--snakefile", os.path.join(config['src'], 'Snakefile'),
                    "-j", "10",
                    "--jobscript","jobscript.sh"
                ],
                stdout=out, stderr=err)

