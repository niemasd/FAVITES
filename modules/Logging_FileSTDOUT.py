#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file and standard output.
'''
from Logging import Logging # abstract Logging class
from Logging_File import Logging_File
import FAVITES_GlobalContext as GC
from os.path import expanduser
from sys import stdout as t

class Logging_FileSTDOUT(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        Logging_File.init()

    def flush():
        Logging_File.flush()
        t.flush()

    def close():
        Logging_File.close()
        t.flush()

    def write(message=''):
        Logging_File.write(message=message)
        t.write(message)
        t.flush()

    def writeln(message=''):
        Logging_File.writeln(message=message)
        t.write(message)
        t.write('\n')
        t.flush()