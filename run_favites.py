#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse                                                   # to parse user arguments
from sys import argv,stdout,stdin                                 # standard input/output
from modules import FAVITES_ModuleFactory as MF

def printMessage():
    '''
    Print author message
    '''
    print("/---------------------------------------------------------------------\\")
    print("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |")
    print("|                        Moshiri & Mirarab 2016                       |")
    print("\\---------------------------------------------------------------------/")

def parseArgs():
    '''
    Parse user arguments. As a developer, if you create any of your own module
    implementations, you should modify the corresponding module argument parser
    and "import ____ module" section of this function accordingly.
    '''

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'), help="Configuration file")
    args = parser.parse_args()

    # import modules and store in global access variables
    print("Reading user input configuration from: %r..." % args.config.name, end='')
    MF.read_config(eval(args.config.read()))
    print(" done")

if __name__ == "__main__":
    # print author message
    printMessage()
    print()

    # initialize global access variables
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parseArgs()

    # run Driver
    MF.modules['Driver'].run()