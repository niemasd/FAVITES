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

# return a list of vertex (out)degrees from a given FAVITES-format contact network file
def degrees(f):
    d = {}
    for line in f:
        if len(line.strip()) == 0 or line[0] == '#':
            continue
        parts = line.split()
        assert len(parts) in {3,5} and parts[0] in {'NODE','EDGE'}, "Malformed contact network file"
        if parts[0] == 'NODE':
            assert len(parts) == 3, "Malformed contact network"
            assert parts[1] not in d, "Duplicate node: %s" % parts[1]
            d[parts[1]] = 0
        else:
            assert len(parts) == 5, "Malformed contact network"
            u,v,du = parts[1],parts[2],parts[4]
            assert du in {'d','u'}, "Malformed contact network"
            assert u in d, "Unexpected node: %s" % u
            assert v in d, "Unexpected node: %s" % v
            d[u] += 1
            if du == 'u':
                d[v] += 1
    return list(d.values())