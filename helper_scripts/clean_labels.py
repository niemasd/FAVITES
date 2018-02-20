#!/usr/bin/env python3
'''
For each read of the given sequence file or each leaf of a given phylogenetic
tree, remove everything from the label except for the contact network
individual's name. Note that this should only be done if each individual only
has one sequence or leaf in the dataset (i.e., only sampled once, and during
that sampling, only a single viral sequence was sampled, and the sequencing
event only generated a single read). Otherwise, you will have duplicate labels.
'''
from sys import stdin,stdout
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default="stdin", help="Input FASTQ/FASTA/Newick File")
parser.add_argument('-o', '--output', required=False, type=str, default="stdout", help="Output FASTQ/FASTA/Newick File")
args,unknown = parser.parse_known_args()
if args.input == "stdin":
    args.input = stdin
else:
    args.input = open(args.input)
if args.output == "stdout":
    args.output = stdout
else:
    args.output = open(args.output,'w')
c = 0; filetype = None
for line in args.input:
    if len(line.strip()) == 0:
        continue
    if c == 0:
        try:
            filetype = {'>':"fasta",'@':"fastq"}[line[0]]
        except KeyError:
            filetype = "newick"
        if filetype[0] == 'n':
            try:
                import dendropy
            except ImportError:
                assert False, "Must install DendroPy (pip install dendropy) for Newick files"
    try:
        if filetype[0] == 'f': # FASTQ/FASTA
            i = c%{'fasta':2,'fastq':4}[filetype]
            if i == 0:
                head = line[1:].split('|')[1]
                if filetype == 'fasta':
                    args.output.write(">%s\n" % head)
                else:
                    args.output.write("@%s\n" % head)
            elif i == 1:
                args.output.write(line)
            elif i == 2:
                args.output.write("+\n")
            elif i == 3:
                args.output.write(line)
        else: # Newick
            tree = dendropy.Tree.get(data=line, schema='newick')
            for n in tree.leaf_node_iter():
                n.taxon = dendropy.datamodel.taxonmodel.Taxon(str(n.taxon).split('|')[1])
            args.output.write("%s" % tree.as_string(schema='newick'))
    except:
        assert False, "Error cleaning labels. Perhaps incorrect file format?"
    c += 1
args.output.close()