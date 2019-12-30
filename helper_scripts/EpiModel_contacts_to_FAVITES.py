#!/usr/bin/env python3
'''
Convert an EpiModel contact network into the FAVITES edge-list format.
'''
from gzip import open as gopen
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--individuals', required=True, type=str, help="EpiModel Individuals (.tsv)")
parser.add_argument('-c', '--contacts', required=True, type=str, help="EpiModel Contacts (.tsv)")
parser.add_argument('-o', '--output', required=False, default='stdout', type=str, help="Output File")
args,unknown = parser.parse_known_args()
output_lines = list()

# parse individuals
if args.individuals.lower().endswith('.gz'):
    lines = gopen(args.individuals).read().decode().splitlines()
else:
    lines = open(args.individuals).readlines()
people = [[v.strip() for v in l.strip().split('\t')] for l in lines if l[0] != '\t']
num_to_name = {p[0]:p[1] for p in people}
for p in people:
    output_lines.append("NODE\t%s\t%s" % (p[1], ','.join(p[2:])))

# parse contacts
if args.contacts.lower().endswith('.gz'):
    lines = gopen(args.contacts).read().decode().splitlines()
else:
    lines = open(args.contacts).readlines()
for l in lines:
    if l[0] == '\t':
        continue
    s,e,u,v = [x.strip() for x in l.split('\t')[1:5]]
    output_lines.append("EDGE\t%s\t%s\t%s,%s\tu" % (num_to_name[u],num_to_name[v],s,e))

# write to output
if args.output.lower().endswith('.gz'):
    f = gopen(args.output,'wb',9); f.write('\n'.join(output_lines).encode()); f.write(b'\n'); f.close()
else:
    if args.output.lower() == 'stdout':
        from sys import stdout as f
    else:
        f = open(args.output,'w')
    f.write('\n'.join(output_lines)); f.write('\n'); f.close()
