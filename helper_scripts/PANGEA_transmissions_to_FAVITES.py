#!/usr/bin/env python3
'''
Convert a PANGEA transmission network into the FAVITES edge-list format.
'''
from sys import stdin
import argparse
PANGEA_HEADER = ['IdInfector', 'IdInfected', 'TimeOfInfection', 'IsInfectorAcute']
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--trans', required=False, type=argparse.FileType('r'), default=stdin, help="PANGEA transmission network (.csv)")
args = parser.parse_args()
for line in args.trans:
    parts = line.strip().split(',')
    if len(parts) == 1 or parts == PANGEA_HEADER:
        continue
    u = parts[0]
    if u == '-1':
        u = 'None'
    v = parts[1]
    t = parts[2]
    print("%s\t%s\t%s" % (u,v,t))