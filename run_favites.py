#! /usr/bin/env python3
'''
FAVITES: FrAmework for VIral Transmission and Evolution Simulation
'''
from modules import FAVITES_ModuleFactory as MF
from modules import FAVITES_GlobalContext as GC
import argparse
from sys import argv,stdout,stdin
from warnings import warn
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
        parser.add_argument('-o', '--out_dir', required=False, type=str, help="Output directory")
        parser.add_argument('-s', '--random_number_seed', required=False, type=int, help="Random number seed")
        parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
        args = parser.parse_args()
        ORIG_CONFIG = args.config.read()
        try:
            config = eval(ORIG_CONFIG)
        except:
            raise SyntaxError("Malformed FAVITES configuration file. Must be valid JSON")
        if args.out_dir is not None:
            if 'out_dir' in config:
                warn("Output directory specified in command line (%s) and config file (%s). Command line will take precedence" % (args.out_dir, config['out_dir']))
            config['out_dir'] = args.out_dir
        assert 'out_dir' in config, "Parameter 'out_dir' is not in the configuration file!"
        environ['out_dir_print'] = config['out_dir']
        config['verbose'] = args.verbose
        if args.random_number_seed is not None:
            if "random_number_seed" in config:
                warn("Random number seed specified in command line (%d) and config file (%s). Command line will take precedence" % (args.random_number_seed, config['random_number_seed']))
            config["random_number_seed"] = args.random_number_seed

    # import modules and store in global access variables
    if "random_number_seed" not in config:
        config["random_number_seed"] = ""

    # update config string based on (potential) updates
    ORIG_CONFIG = str(config)

    # set verbosity
    MF.read_config(config, config['verbose'])
    GC.VERBOSE = config['verbose']

if __name__ == "__main__":
    # initialize global access variables
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parseArgs()

    # run Driver
    MF.modules['Driver'].run('/'.join(expanduser(abspath(argv[0])).split('/')[:-1]), ORIG_CONFIG)