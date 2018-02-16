#!/usr/bin/env python3
'''
For each read of the given sequence file, remove everything from the read's
header except for the contact network individual's name. Note that this should
only be done if each individual only has one sequence in the dataset (i.e., only
sampled once, and during that sampling, only a single viral sequence was
sampled, and the sequencing event only generated a single read).
'''
from sys import stdin,stdout
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default="stdin", help="Input FASTQ File")
parser.add_argument('-o', '--output', required=False, type=str, default="stdout", help="Output FASTQ File")
args,unknown = parser.parse_known_args()
if args.input == "stdin":
    args.input = stdin
else:
    args.input = open(args.input)
if args.output == "stdout":
    args.output = stdout
else:
    args.output = open(args.output,'w')
c = 0; fasta = None
for line in args.input:
    if c == 0:
        fasta = {'>':True,'@':False}[line[0]]
    i = c%{True:2,False:4}[fasta]
    if i == 0:
        head = line[1:].split('|')[1]
        if fasta:
            args.output.write(">%s\n" % head)
        else:
            args.output.write("@%s\n" % head)
    elif i == 1:
        args.output.write(line)
    elif i == 2:
        args.output.write("+\n")
    elif i == 3:
        args.output.write(line)
    c += 1
args.output.close()