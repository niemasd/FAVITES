#! /usr/bin/env python3
'''
FAVITES: FrAmework for VIral Transmission and Evolution Simulation
'''
import argparse
from json import loads
from os import makedirs
from os.path import abspath,expanduser,isdir,isfile
from sys import platform,stderr
from subprocess import call,check_output,CalledProcessError,STDOUT
from tempfile import NamedTemporaryFile
from warnings import warn
from urllib.error import URLError
from urllib.request import urlopen
DOCKER_IMAGE = "niemasd/favites"
MAIN_VERSION_SYMBOLS = {'0','1','2','3','4','5','6','7','8','9','.'}

# return True if the given tag (string) is a main version (e.g. '1.1.1') or False if not (e.g. '1.1.1a')
def is_main_version(tag):
    for c in tag:
        if c not in MAIN_VERSION_SYMBOLS:
            return False
    return True

# get the latest FAVITES Docker image main version
def get_latest_version():
    try:
        DOCKER_TAGS = list(); curr_url = "https://hub.docker.com/v2/repositories/%s/tags/?page=1" % DOCKER_IMAGE
        while curr_url is not None:
            tmp = loads(urlopen(curr_url).read().decode('utf-8'))
            DOCKER_TAGS += [e['name'] for e in tmp['results']]
            curr_url = tmp['next']
        DOCKER_TAGS = [tag for tag in DOCKER_TAGS if is_main_version(tag)] # remove non-main-version
        DOCKER_TAGS = [tuple(int(i) for i in tag.split('.')) for tag in DOCKER_TAGS] # convert to tuple of ints
        DOCKER_TAGS.sort() # sort in ascending order
        return '.'.join(str(i) for i in DOCKER_TAGS[-1])
    except Exception as e:
        raise RuntimeError("Failed to use Python 3 urllib to connect to FAVITES Docker repository webpage\n%s" % str(e))

# if Mac OS X, use portable TMPDIR
if platform == 'darwin':
    from os import environ
    environ['TMPDIR'] = '/tmp/docker_tmp'

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--config', required=True, type=str, help="Configuration file")
parser.add_argument('-o', '--out_dir', required=False, type=str, help="Output directory")
parser.add_argument('-s', '--random_number_seed', required=False, type=int, help="Random number seed")
parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
parser.add_argument('-u', '--update', nargs='*', help="Update Docker image (-u to pull newest version, -u <VERSION> to pull <VERSION>)")
args = parser.parse_args()

# check user args
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
    assert isfile(CN_FILE), "File not found: %s" % CONFIG_DICT['contact_network_file']
    CONFIG_DICT['contact_network_file'] = '/FAVITES_MOUNT/%s' % CN_FILE.split('/')[-1]
TN_FILE = None
if 'transmission_network_file' in CONFIG_DICT:
    TN_FILE = abspath(expanduser(CONFIG_DICT['transmission_network_file']))
    assert isfile(TN_FILE), "File not found: %s" % CONFIG_DICT['transmission_network_file']
    CONFIG_DICT['transmission_network_file'] = '/FAVITES_MOUNT/%s' % TN_FILE.split('/')[-1]
SAMPLE_TIME_FILE = None
if 'sample_time_file' in CONFIG_DICT:
    SAMPLE_TIME_FILE = abspath(expanduser(CONFIG_DICT['sample_time_file']))
    assert isfile(SAMPLE_TIME_FILE), "File not found: %s" % CONFIG_DICT['sample_time_file']
    CONFIG_DICT['sample_time_file'] = '/FAVITES_MOUNT/%s' % SAMPLE_TIME_FILE.split('/')[-1]
TREE_FILE = None
if 'tree_file' in CONFIG_DICT:
    TREE_FILE = abspath(expanduser(CONFIG_DICT['tree_file']))
    assert isfile(TREE_FILE), "File not found: %s" % CONFIG_DICT['tree_file']
    CONFIG_DICT['tree_file'] = '/FAVITES_MOUNT/%s' % TREE_FILE.split('/')[-1]
ERRORFREE_SEQ_FILE = None
if 'errorfree_sequence_file' in CONFIG_DICT:
    ERRORFREE_SEQ_FILE = abspath(expanduser(CONFIG_DICT['errorfree_sequence_file']))
    assert isfile(ERRORFREE_SEQ_FILE), "File not found: %s" % CONFIG_DICT['errorfree_sequence_file']
    CONFIG_DICT['errorfree_sequence_file'] = '/FAVITES_MOUNT/%s' % ERRORFREE_SEQ_FILE.split('/')[-1]
HMMBUILD_MSA_FILE = None
if 'hmmbuild_msafile' in CONFIG_DICT:
    HMMBUILD_MSA_FILE = abspath(expanduser(CONFIG_DICT['hmmbuild_msafile']))
    assert isfile(HMMBUILD_MSA_FILE), "File not found: %s" % CONFIG_DICT['hmmbuild_msafile']
    CONFIG_DICT['hmmbuild_msafile'] = '/FAVITES_MOUNT/%s' % HMMBUILD_MSA_FILE.split('/')[-1]
TMP_CONFIG = NamedTemporaryFile('w')
TMP_CONFIG.write(str(CONFIG_DICT).replace(": inf",": float('inf')"))
TMP_CONFIG.flush()

# pull the newest versioned Docker image (if applicable)
if args.update is None:
    version = None
    try:
        o = check_output(['docker','images']).decode().splitlines()
        for l in o:
            if l.startswith(DOCKER_IMAGE):
                version = '%s:%s' % (DOCKER_IMAGE,l.split()[1]); break
    except CalledProcessError as e:
        raise RuntimeError("docker images command failed\n%s"%e.output)
    if version is None:
        args.update = []
if args.update is not None:
    assert len(args.update) < 2, "More than one Docker image version specified. Must either specify just -u or -u <VERSION>"
    if len(args.update) == 0:
        tag = get_latest_version()
    else:
        tag = args.update[0]
    version = '%s:%s'%(DOCKER_IMAGE,tag)
    try:
        need_to_pull = True
        if tag != 'latest':
            o = check_output(['docker','images']).decode().splitlines()
            for l in o:
                if l.startswith(DOCKER_IMAGE) and l.split()[1] == version.split(':')[1]:
                    need_to_pull = False; break
    except CalledProcessError as e:
        raise RuntimeError("docker images command failed\n%s"%e.output)
    if need_to_pull:
        print("Pulling Docker image (%s)..." % tag, end=' ', file=stderr); stderr.flush()
        try:
            o = check_output(['docker','pull',version], stderr=STDOUT)
            print("done", file=stderr); stderr.flush()
        except Exception as e:
            if "manifest for %s not found"%version in e.output.decode():
                raise ValueError("Invalid FAVITES version specified: %s"%tag)
            else:
                raise RuntimeError("docker pull command failed\n%s"%e.output)
        try:
            print("Removing old Docker images...", end=' ', file=stderr); stderr.flush()
            o = check_output(['docker','images']).decode().splitlines()
            for l in o:
                if l.startswith(DOCKER_IMAGE):
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
            response = input("ERROR: Output directory exists. Overwrite? All contents will be deleted. (y/n) ").strip().lower()
            if response[0] == 'y':
                from shutil import rmtree
                rmtree(OUTPUT_DIR); makedirs(OUTPUT_DIR)
            else:
                exit(-1)

# call Docker image for user
COMMAND =  ['docker','run',]                                          # Docker command
COMMAND += ['-v',TMP_CONFIG.name+':/FAVITES_MOUNT/USER_CONFIG.JSON']  # mount config file
COMMAND += ['-v',OUTPUT_DIR+':/FAVITES_MOUNT/OUTPUT_DIR']             # mount output directory
COMMAND += ['-v',TMP_CONFIG.name+':/USER_CONFIG.JSON']                # compatibility for older Docker images
COMMAND += ['-v',OUTPUT_DIR+':/OUTPUT_DIR']
if CN_FILE is not None:                                               # mount contact network file (if need be)
    COMMAND += ['-v',CN_FILE+':'+CONFIG_DICT['contact_network_file']]
if TN_FILE is not None:                                               # mount transmission network file (if need be)
    COMMAND += ['-v',TN_FILE+':'+CONFIG_DICT['transmission_network_file']]
if SAMPLE_TIME_FILE is not None:
    COMMAND += ['-v',SAMPLE_TIME_FILE+':'+CONFIG_DICT['sample_time_file']]
if TREE_FILE is not None:
    COMMAND += ['-v',TREE_FILE+':'+CONFIG_DICT['tree_file']]
if ERRORFREE_SEQ_FILE is not None:
    COMMAND += ['-v',ERRORFREE_SEQ_FILE+':'+CONFIG_DICT['errorfree_sequence_file']]
if HMMBUILD_MSA_FILE is not None:
    COMMAND += ['-v',HMMBUILD_MSA_FILE+':'+CONFIG_DICT['hmmbuild_msafile']]
if not platform.startswith('win'):                                    # if not Windows,
    from os import geteuid,getegid
    COMMAND += ['-u',str(geteuid())+':'+str(getegid())]               # make output files owned by user instead of root
COMMAND += [version]                                                  # Docker image
try:
    if args.verbose:
        print("\n\nRunning FAVITES Docker command:\n%s\n\n" % ' '.join(COMMAND))
    call(COMMAND)
except:
    exit(-1)
TMP_CONFIG.close()
