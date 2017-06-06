#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to standard output.
'''
from Logging import Logging # abstract Logging class
from sys import stdout as s
import FAVITES_GlobalContext as GC

class Logging_STDOUT(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def flush():
        s.flush()

    def close():
        s.flush()

    def write(message=''):
        s.write(message)
        s.flush()

    def writeln(message=''):
        s.write(message)
        s.write('\n')
        s.flush()