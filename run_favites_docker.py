#! /usr/bin/env python3
import argparse
from os import makedirs
from os.path import abspath,expanduser,isfile
from subprocess import call

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
args = parser.parse_args()

# check user args
CONFIG = expanduser(abspath(args.config))
assert isfile(args.config), "ERROR: Cannot open configuration file: %s" % args.config
OUTPUT_DIR = expanduser(abspath(eval(open(CONFIG).read())['out_dir']))
makedirs(OUTPUT_DIR)

# call Docker image for user
COMMAND =  ['docker','run',]                  # Docker command
COMMAND += ['-v',CONFIG+':/USER_CONFIG.JSON'] # mount config file
COMMAND += ['-v',OUTPUT_DIR+':/OUTPUT_DIR']   # mount output directory
COMMAND += ['niemasd/favites']                # Docker image
call(COMMAND)