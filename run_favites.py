#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse
from sys import argv,stdout,stdin
from modules import FAVITES_ModuleFactory as MF

def printMessage():
    '''
    Print author message
    '''
    stdout.write("/---------------------------------------------------------------------\\\n")
    stdout.write("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |\n")
    stdout.write("|                        Moshiri & Mirarab 2016                       |\n")
    stdout.write("\\---------------------------------------------------------------------/\n")
    stdout.flush()

def parseArgs():
    '''
    Parse user arguments. As a developer, if you create any of your own module
    implementations, you should modify the corresponding module argument parser
    and "import ____ module" section of this function accordingly.
    '''

    # print author message
    printMessage()
    stdout.write('\n')

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'), help="Configuration file")
    args = parser.parse_args()

    # import modules and store in global access variables
    stdout.write("Reading user input configuration from: %r..." % args.config.name)
    stdout.flush()
    MF.read_config(eval(args.config.read()))
    stdout.write(" done\n")
    stdout.flush()

if __name__ == "__main__":
    # initialize global access variables
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parseArgs()

    # run Driver
    MF.modules['Driver'].run()