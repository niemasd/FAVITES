#! /usr/bin/env python3
import argparse
from os import makedirs
from os.path import abspath,expanduser,isdir,isfile
from sys import platform,stderr
from subprocess import call,DEVNULL,STDOUT

# pull the latest Docker image
print("Pulling latest Docker image...", end=' ', file=stderr); stderr.flush()
call(['docker','pull','niemasd/favites'], stdout=DEVNULL, stderr=STDOUT)
print("done", file=stderr)

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
args = parser.parse_args()

# check user args
CONFIG = abspath(expanduser(args.config))
assert isfile(CONFIG), "ERROR: Cannot open configuration file: %s" % CONFIG
try:
    CONFIG_DICT = eval(open(CONFIG).read())
except:
    raise SyntaxError("Malformed FAVITES configuration file. Must be valid JSON")
assert 'out_dir' in CONFIG_DICT, "Parameter 'out_dir' is not in the configuration file!"
OUTPUT_DIR = abspath(CONFIG_DICT['out_dir'])

# create output directory
try:
    makedirs(OUTPUT_DIR)
except:
    if isdir(OUTPUT_DIR):
        response = 'x'
        while len(response) == 0 or response[0] not in {'y','n'}:
            response = input("ERROR: Output directory exists. Overwrite? All contents will be deleted. (y/n)").strip().lower()
            if response[0] == 'y':
                from shutil import rmtree
                rmtree(OUTPUT_DIR); makedirs(OUTPUT_DIR)
            else:
                exit(-1)

# call Docker image for user
COMMAND =  ['docker','run',]                            # Docker command
COMMAND += ['-v',CONFIG+':/USER_CONFIG.JSON']           # mount config file
COMMAND += ['-v',OUTPUT_DIR+':/OUTPUT_DIR']             # mount output directory
if not platform.startswith('win'):                      # if not Windows,
    from os import geteuid,getegid
    COMMAND += ['-u',str(geteuid())+':'+str(getegid())] # make output files owned by user instead of root
COMMAND += ['niemasd/favites']                          # Docker image
call(COMMAND)