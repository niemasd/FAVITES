#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file and standard output.
'''
from Logging import Logging # abstract Logging class
import FAVITES_GlobalContext as GC
from os.path import expanduser
from sys import stdout as t

class Logging_FileSTDOUT(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        global s
        s = open(expanduser(GC.log_file),'w')

    def flush():
        s.flush()
        t.flush()

    def close():
        s.close()
        t.flush()

    def write(message=''):
        s.write(message)
        s.flush()
        t.write(message)
        t.flush()

    def writeln(message=''):
        s.write(message)
        s.write('\n')
        s.flush()
        t.write(message)
        t.write('\n')
        t.flush()