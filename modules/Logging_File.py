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
    def set_stream():
        if s is None:
            s = open(GC.out_dir + '/' + LOG_FILE,'w')

    def cite():
        return GC.CITATION_FAVITES

    def init():
        global s
        s = None

    def flush():
        Logging_File.set_stream()
        s.flush()

    def close():
        Logging_File.set_stream()
        s.close()

    def write(message=''):
        Logging_File.set_stream()
        s.write(message)
        s.flush()

    def writeln(message=''):
        Logging_File.set_stream()
        s.write(message)
        s.write('\n')
        s.flush()