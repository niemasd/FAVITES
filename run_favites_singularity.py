#! /usr/bin/env python3
'''
FAVITES: FrAmework for VIral Transmission and Evolution Simulation
'''
import argparse
import os
from glob import glob
from os import chdir,getcwd,makedirs,symlink
from os.path import abspath,expanduser,isdir,isfile
from shutil import move
from subprocess import call,check_output,CalledProcessError,DEVNULL,STDOUT
from sys import platform,stderr,stdout
from tempfile import NamedTemporaryFile,TemporaryDirectory
from warnings import warn
from urllib.error import URLError
from urllib.request import urlopen
DOCKER_IMAGE = "docker://niemasd/favites"
MAIN_VERSION_SYMBOLS = {'0','1','2','3','4','5','6','7','8','9','.'}
INCOMPATIBLE = {'1.0.0','1.0.1','1.0.2','1.0.3','1.1.0','1.1.1','1.1.2','1.1.3','1.1.4','1.1.5','1.1.6'}

# return True if the given tag (string) is a main version (e.g. '1.1.1') or False if not (e.g. '1.1.1a')
def is_main_version(tag):
    for c in tag:
        if c not in MAIN_VERSION_SYMBOLS:
            return False
    return True

# get the latest FAVITES Docker image main version
def get_latest_version():
    try:
        DOCKER_TAGS = [t for t in urlopen("https://hub.docker.com/r/niemasd/favites/tags/").read().decode('utf-8').split('"tags":')[1].split(':')[-1][1:-2].replace('"','').split(',') if '.' in t]
        DOCKER_TAGS = [tag for tag in DOCKER_TAGS if is_main_version(tag)] # remove non-main-version
        DOCKER_TAGS = [tuple(int(i) for i in tag.split('.')) for tag in DOCKER_TAGS] # convert to tuple of ints
        DOCKER_TAGS.sort() # sort in ascending order
        return '.'.join(str(i) for i in DOCKER_TAGS[-1])
    except Exception as e:
        raise RuntimeError("Failed to use Python 3 urllib to connect to FAVITES Docker repository webpage\n%s"%str(e))

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-o', '--out_dir', required=False, type=str, help="Output directory")
parser.add_argument('-s', '--random_number_seed', required=False, type=int, help="Random number seed")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
parser.add_argument('-u', '--update', required=True, nargs='*', help="Update Docker image (-u to pull newest version, -u <VERSION> to pull <VERSION>)")
args = parser.parse_args()

# check user args
TMPDIR = TemporaryDirectory()
CONFIG = abspath(expanduser(args.config))
assert isfile(CONFIG), "ERROR: Cannot open configuration file: %s" % CONFIG
try:
    CONFIG_DICT = eval(open(CONFIG).read())
except:
    raise SyntaxError("Malformed FAVITES configuration file. Must be valid JSON")
if args.out_dir is not None:
    if 'out_dir' in CONFIG_DICT:
        warn("Output directory specified in command line (%s) and config file (%s). Command line will take precedence" % (args.out_dir, CONFIG_DICT['out_dir']))
    CONFIG_DICT['out_dir'] = args.out_dir
assert 'out_dir' in CONFIG_DICT, "Parameter 'out_dir' is not in the configuration file!"
OUTPUT_DIR = abspath(expanduser(CONFIG_DICT['out_dir']))
if args.random_number_seed is not None:
    if "random_number_seed" in CONFIG_DICT:
        warn("Random number seed specified in command line (%d) and config file (%s). Command line will take precedence" % (args.random_number_seed, CONFIG_DICT['random_number_seed']))
    CONFIG_DICT["random_number_seed"] = args.random_number_seed
if "random_number_seed" not in CONFIG_DICT:
    CONFIG_DICT["random_number_seed"] = ""
CN_FILE = None
if 'contact_network_file' in CONFIG_DICT:
    CN_FILE = abspath(expanduser(CONFIG_DICT['contact_network_file']))
    CONFIG_DICT['contact_network_file'] = '/FAVITES_MOUNT/%s' % CN_FILE.split('/')[-1]
    symlink(CN_FILE, '%s/%s' % (TMPDIR.name, CN_FILE.split('/')[-1]))
TN_FILE = None
if 'transmission_network_file' in CONFIG_DICT:
    TN_FILE = abspath(expanduser(CONFIG_DICT['transmission_network_file']))
    CONFIG_DICT['transmission_network_file'] = '/FAVITES_MOUNT/%s' % TN_FILE.split('/')[-1]
    symlink(TN_FILE, '%s/%s' % (TMPDIR.name, TN_FILE.split('/')[-1]))
TREE_FILE = None
if 'tree_file' in CONFIG_DICT:
    TREE_FILE = abspath(expanduser(CONFIG_DICT['tree_file']))
    CONFIG_DICT['tree_file'] = '/FAVITES_MOUNT/%s' % TREE_FILE.split('/')[-1]
    symlink(TREE_FILE, '%s/%s' % (TMPDIR.name, TREE_FILE.split('/')[-1]))
ERRORFREE_SEQ_FILE = None
if 'errorfree_sequence_file' in CONFIG_DICT:
    ERRORFREE_SEQ_FILE = abspath(expanduser(CONFIG_DICT['errorfree_sequence_file']))
    CONFIG_DICT['errorfree_sequence_file'] = '/FAVITES_MOUNT/%s' % ERRORFREE_SEQ_FILE.split('/')[-1]
    symlink(ERRORFREE_SEQ_FILE, '%s/%s' % (TMPDIR.name, ERRORFREE_SEQ_FILE.split('/')[-1]))
TMP_CONFIG = NamedTemporaryFile('w')
TMP_CONFIG.write(str(CONFIG_DICT))
TMP_CONFIG.flush()
symlink(TMP_CONFIG.name, '%s/USER_CONFIG.JSON' % TMPDIR.name)

# pull the newest versioned Docker image (if applicable)
if args.update is not None:
    assert len(args.update) < 2, "More than one Docker image version specified. Must either specify just -u or -u <VERSION>"
    if len(args.update) == 0:
        tag = get_latest_version()
    else:
        tag = args.update[0]
        assert tag not in INCOMPATIBLE, "Using incompatible version (%s). Singularity is only supported in FAVITES 1.1.7 onward"%tag
    version = '%s:%s'%(DOCKER_IMAGE,tag)

# create output directory
try:
    makedirs(OUTPUT_DIR)
except:
    if isdir(OUTPUT_DIR):
        response = 'x'
        while len(response) == 0 or response[0] not in {'y','n'}:
            response = input("ERROR: Output directory exists. Overwrite? All contents will be deleted. (y/n) ").strip().lower()
            if response[0] == 'y':
                from shutil import rmtree
                rmtree(OUTPUT_DIR); makedirs(OUTPUT_DIR)
            else:
                exit(-1)
symlink(OUTPUT_DIR, '%s/OUTPUT_DIR' % TMPDIR.name)

# first pull Docker image as Singularity image
pulled_image = expanduser('~/.favites/singularity-favites-%s.img'%tag)
if not isfile(pulled_image):
    with TemporaryDirectory() as pull_dir:
        orig_dir = getcwd()
        chdir(pull_dir)
        print("Pulling Docker image...", end=' '); stdout.flush()
        check_output(['singularity','pull',version], stderr=DEVNULL)
        makedirs(expanduser('~/.favites'), exist_ok=True)
        for f in glob('*.img'):
            move(f,pulled_image); break
        chdir(orig_dir)
        print("done"); stdout.flush()

# set up Docker command and run
COMMAND =  ['singularity','run','-e']              # Singularity command
COMMAND += ['-B',TMPDIR.name+':/FAVITES_MOUNT:rw'] # mount output directory
COMMAND += [pulled_image]                          # Docker image
call(COMMAND)
TMP_CONFIG.close()
