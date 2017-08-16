#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
from modules import FAVITES_ModuleFactory as MF
from modules import FAVITES_GlobalContext as GC
import argparse
from sys import argv,stdout,stdin
from os import environ,getcwd
from os.path import abspath,expanduser,isdir

def parseArgs():
    '''
    Parse user arguments. As a developer, if you create any of your own module
    implementations, you should modify the corresponding module argument parser
    and "import ____ module" section of this function accordingly.
    '''
    global ORIG_CONFIG

    # if running in Docker image, hardcode config and output directory
    if 'FAVITES_DOCKER' in environ:
        ORIG_CONFIG = open('/USER_CONFIG.JSON').read()
        config = eval(ORIG_CONFIG)
        assert 'out_dir' in config, "Parameter 'out_dir' is not in the configuration file!"
        environ['out_dir_print'] = config['out_dir']
        config['out_dir'] = '/OUTPUT_DIR'
        if 'verbose' not in config: # Add "verbose":True to config for verbosity
            config['verbose'] = False

    # use argparse to parse user arguments
    else:
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'), help="Configuration file")
        parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
        args = parser.parse_args()
        ORIG_CONFIG = args.config.read()
        config = eval(ORIG_CONFIG)
        assert 'out_dir' in config, "Parameter 'out_dir' is not in the configuration file!"
        environ['out_dir_print'] = config['out_dir']
        assert not isdir(abspath(expanduser(config['out_dir']))), "ERROR: Output directory exists"
        config['verbose'] = args.verbose

    # import modules and store in global access variables
    MF.read_config(config, config['verbose'])
    GC.VERBOSE = config['verbose']

if __name__ == "__main__":
    # initialize global access variables
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parseArgs()

    # run Driver
    MF.modules['Driver'].run('/'.join(expanduser(abspath(argv[0])).split('/')[:-1]), ORIG_CONFIG)