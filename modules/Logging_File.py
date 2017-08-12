#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file.
'''
from Logging import Logging # abstract Logging class
import FAVITES_GlobalContext as GC
from os.path import expanduser

LOG_FILE = 'FAVITES.log'

class Logging_File(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        global s
        s = open(LOG_FILE,'w')

    def flush():
        s.flush()

    def close():
        s.close()

    def write(message=''):
        s.write(message)
        s.flush()

    def writeln(message=''):
        s.write(message)
        s.write('\n')
        s.flush()