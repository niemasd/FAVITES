#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file and standard error.
'''
from Logging import Logging # abstract Logging class
from Logging_File import Logging_File
from Logging_STDERR import Logging_STDERR
import FAVITES_GlobalContext as GC

class Logging_FileSTDERR(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        Logging_File.init()
        Logging_STDERR.init()

    def flush():
        Logging_File.flush()
        Logging_STDERR.flush()

    def close():
        Logging_File.close()
        Logging_STDERR.close()

    def write(message=''):
        Logging_File.write(message=message)
        Logging_STDERR.write(message=message)

    def writeln(message=''):
        Logging_File.writeln(message=message)
        Logging_STDERR.writeln(message=message)