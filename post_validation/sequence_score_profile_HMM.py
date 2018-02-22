#! /usr/bin/env python3
'''
Niema Moshiri 2017

Score each given sequence against a given profile HMM.
'''
from common import readFASTQ
from os.path import isfile
from subprocess import CalledProcessError,check_output
import argparse

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-H', '--HMM', required=True, type=str, help="Profile HMM")
parser.add_argument('-s', '--seq', required=True, type=str, help="Sequences")
parser.add_argument('-p', '--cpu', required=False, type=int, default=1, help="Number of CPUs")
parser.add_argument('-q', '--fastq', action='store_true', help="Input file is FASTQ (not FASTA)")
parser.add_argument('-a', '--hmmsearch', required=False, type=str, default='hmmsearch', help="Path to hmmsearch")
args,unknown = parser.parse_known_args()
assert isfile(args.HMM), "ERROR: Invalid file: %s" % args.HMM
assert isfile(args.seq), "ERROR: Invalid file: %s" % args.seq

# if user specified FASTQ, convert to FASTA
if args.fastq:
    from tempfile import NamedTemporaryFile
    seqs = readFASTQ(open(args.seq))
    tmp = NamedTemporaryFile(mode='w')
    tmp.write('\n'.join([">%s\n%s" % (ID,seqs[ID][0]) for ID in seqs]))
    tmp.flush()
    args.seq = tmp.name

# perform alignment
try:
    s = check_output([args.hmmsearch,'--cpu',str(args.cpu),'--noali','--notextw',args.HMM,args.seq]).decode()
except CalledProcessError as e:
    print(e.output.decode())
    exit(1)
print('ID,E-value,score,bias')
for entry in s.split('//'):
    if len(entry) < 10: # ending [ok] line
        continue
    lines = [l.strip() for l in entry.strip().splitlines() if len(l) > 0 and l[0] != '#']
    if len(lines) < 5: # header HMMER line
        continue
    queryline = -1; scoreline = -1
    for i in range(len(lines)):
        if lines[i].startswith('Query:'):
            queryline = i; scoreline = i+5
    if queryline == -1:
        continue
    query = lines[queryline].split()[1]
    evalue,score,bias = lines[scoreline].split()[:3]
    print("%s,%s,%s,%s" % (query,evalue,score,bias))
