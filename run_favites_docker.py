#! /usr/bin/env python3
import argparse
from os import makedirs
from os.path import abspath,expanduser,isdir,isfile
from sys import platform,stderr
from subprocess import call,check_output,CalledProcessError,STDOUT

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
parser.add_argument('-u', '--update', nargs='*', help="Update Docker image (-u to pull latest, -u <VERSION> to pull <VERSION>)")
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

# pull the latest Docker image (if applicable)
try:
	has_image = False
	o = check_output(['docker','images']).decode().splitlines()
	for l in o:
		if l.startswith('niemasd/favites'):
			has_image = True; break
	if not has_image:
		args.update = []
except CalledProcessError as e:
	raise RuntimeError("docker images command failed\n%s"%e.output)
if args.update is not None:
	assert len(args.update) < 2, "More than one Docker image version specified. Must either specify just -u or -u <VERSION>"
	if len(args.update) == 0:
		tag = 'latest'
	else:
		tag = args.update[0]
	version = 'niemasd/favites:%s'%tag
	print("Pulling Docker image (%s)..." % tag, end=' ', file=stderr); stderr.flush()
	try:
		o = check_output(['docker','pull',version], stderr=STDOUT)
	except CalledProcessError as e:
		if "manifest for %s not found"%version in e.output.decode():
			raise ValueError("Invalid FAVITES version specified: %s"%tag)
		else:
			raise RuntimeError("docker pull command failed\n%s"%e.output)
	# try to remove old images
	try:
		o = check_output(['docker','images']).decode().splitlines()
		for l in o:
			if l.startswith('niemasd/favites'):
				p = l.split()
				if tag != p[1]:
					check_output(['docker','image','rm','--force',p[2]])
		print("done", file=stderr)
	except:
		print("Failed to remove old Docker images", file=stderr); stderr.flush()

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
try:
	call(COMMAND)
except:
	exit(-1)
