#! /usr/bin/env python3
'''
Niema Moshiri 2017

Common functions
'''
# compute the average of list x
def avg(x):
    return sum(x)/float(len(x))

# read FASTQ stream and return (ID,(seq,qual)) dictionary
def readFASTQ(stream):
    seqs = {}
    name = None
    seq = ''; qual = ''
    i = 0
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if i%4 == 0:
            if name is not None:
                assert len(seq) != 0, "Malformed FASTQ"
                seqs[name] = (seq,qual)
            name = l[1:]
            assert name not in seqs, "Duplicate sequence ID: %s" % name
            seq = ''; qual = ''
        elif i%4 == 1:
            seq += l
        elif i%4 == 3:
            qual += l
        i += 1
        assert name is not None and len(seq) != 0, "Malformed FASTQ"
    seqs[name] = (seq,qual)
    return seqs