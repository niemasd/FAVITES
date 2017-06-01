#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse
from sys import argv,stdout,stdin
from os import getcwd
from modules import FAVITES_ModuleFactory as MF
from modules import FAVITES_GlobalContext as GC

def parseArgs():
    '''
    Parse user arguments. As a developer, if you create any of your own module
    implementations, you should modify the corresponding module argument parser
    and "import ____ module" section of this function accordingly.
    '''

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'), help="Configuration file")
    parser.add_argument('-v', '--verbose', action="store_true", help="Print verbose messages to stderr")
    args = parser.parse_args()

    # import modules and store in global access variables
    MF.read_config(eval(args.config.read()), args.verbose)
    GC.VERBOSE = args.verbose

if __name__ == "__main__":
    # initialize global access variables
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parseArgs()

    # run Driver
    MF.modules['Driver'].run()