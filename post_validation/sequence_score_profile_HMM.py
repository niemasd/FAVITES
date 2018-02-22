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
IDs = {l.strip()[1:] for l in open(args.seq) if l[0] == '>'}

# perform alignment
try:
    s = check_output([args.hmmsearch,'--cpu',str(args.cpu),'--noali','--notextw','-T','0',args.HMM,args.seq]).decode()
except CalledProcessError as e:
    print(e.output.decode())
    exit(1)
s = s.split('Scores for complete sequences')[1].split('Domain annotation for each sequence')[0].splitlines()[4:]
print('ID,E-value,score,bias')
for line in s:
    l = line.strip()
    if len(l) == 0:
        continue
    try:
        parts = l.split(); evalue,score,bias = parts[:3]; query = parts[8]; IDs.remove(query)
        print("%s,%s,%s,%s" % (query,evalue,score,bias))
    except KeyError:
        continue
for ID in IDs:
    print("%s,inf,0,0"%ID)