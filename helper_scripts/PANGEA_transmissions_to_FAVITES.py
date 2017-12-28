#!/usr/bin/env python3
'''
Convert a PANGEA transmission network into the FAVITES edge-list format.
'''
from sys import stdout
import argparse
PANGEA_HEADER = ['IdInfector', 'IdInfected', 'TimeOfInfection', 'IsInfectorAcute']
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), help="PANGEA transmission network (.csv)")
parser.add_argument('-o', '--output', required=False, default=stdout, type=argparse.FileType('w'), help="Output File")
args,unknown = parser.parse_known_args()
for line in args.input:
    parts = line.strip().split(',')
    if len(parts) == 1 or parts == PANGEA_HEADER:
        continue
    u = parts[0]
    if u[0] == '-':
        u = 'None'
    v = parts[1]
    t = parts[2]
    args.output.write("%s\t%s\t%s\n" % (u,v,t))