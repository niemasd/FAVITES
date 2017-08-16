#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file.
'''
from Logging import Logging # abstract Logging class
import FAVITES_GlobalContext as GC
from os.path import expanduser

LOG_FILE = 'FAVITES.log'

def set_stream():
    if GC.log_stream is None:
        GC.log_stream = open(LOG_FILE,'w')

class Logging_File(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.log_stream = None

    def flush():
        set_stream()
        GC.log_stream.flush()

    def close():
        set_stream()
        GC.log_stream.close()

    def write(message=''):
        set_stream()
        GC.log_stream.write(message)
        GC.log_stream.flush()

    def writeln(message=''):
        set_stream()
        GC.log_stream.write(message)
        GC.log_stream.write('\n')
        GC.log_stream.flush()