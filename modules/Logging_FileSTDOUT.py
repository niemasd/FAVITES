#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where log messages are written to file and standard output.
'''
from Logging import Logging # abstract Logging class
from Logging_File import Logging_File
from Logging_STDOUT import Logging_STDOUT
import FAVITES_GlobalContext as GC

class Logging_FileSTDOUT(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        Logging_File.init()
        Logging_STDOUT.init()

    def flush():
        Logging_File.flush()
        Logging_STDOUT.flush()

    def close():
        Logging_File.close()
        Logging_STDOUT.close()

    def write(message=''):
        Logging_File.write(message=message)
        Logging_STDOUT.write(message=message)

    def writeln(message=''):
        Logging_File.writeln(message=message)
        Logging_STDOUT.writeln(message=message)