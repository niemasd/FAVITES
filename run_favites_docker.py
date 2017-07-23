#! /usr/bin/env python3
import argparse
from os import geteuid,getegid,makedirs
from os.path import abspath,expanduser,isfile
from sys import stderr
from subprocess import call,DEVNULL,STDOUT

# pull the latest Docker image
print("Pulling latest Docker image...", end=' ', file=stderr)
call(['docker','pull','niemasd/favites'], stdout=DEVNULL, stderr=STDOUT)
print("done", file=stderr)

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
args = parser.parse_args()

# check user args
CONFIG = abspath(expanduser(args.config))
assert isfile(args.config), "ERROR: Cannot open configuration file: %s" % args.config
OUTPUT_DIR = abspath(expanduser(eval(open(CONFIG).read())['out_dir']))
assert not isfile(OUTPUT_DIR), "ERROR: Output directory exists"
makedirs(OUTPUT_DIR)

# call Docker image for user
COMMAND =  ['docker','run',]                        # Docker command
COMMAND += ['-v',CONFIG+':/USER_CONFIG.JSON']       # mount config file
COMMAND += ['-v',OUTPUT_DIR+':/OUTPUT_DIR']         # mount output directory
COMMAND += ['-u',str(geteuid())+':'+str(getegid())] # make output files owned by user instead of root
COMMAND += ['niemasd/favites']                      # Docker image
call(COMMAND)
