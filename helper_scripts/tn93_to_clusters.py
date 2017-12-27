#!/usr/bin/env python3
'''
Convert tn93 output to ClusterPicker cluster format
'''
# parse args
from sys import stdin
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input (tn93 Output CSV")
parser.add_argument('-t', '--threshold', required=False, type=float, default=float('inf'), help="Distance Threshold")
args = parser.parse_args()
assert args.threshold >= 0, "ERROR: Length threshold must be at least 0"
if args.input == 'stdin':
    from sys import stdin; infile = stdin
else:
    infile = open(args.input)

# build graph
g = {} # g[node] = set of neighbors of node
for line in infile:
    l = line.strip()
    if l == 'ID1,ID2,Distance':
        continue
    u,v,d = l.split(',')
    if u not in g:
        g[u] = set()
    if v not in g:
        g[v] = set()
    if float(d) > args.threshold:
        continue
    g[u].add(v); g[v].add(u)

# output clusters
from queue import Queue
explore = set(g.keys()); CLUST = 0
print("SequenceName\tClusterNumber")
while len(explore) != 0:
    curr = explore.pop(); cluster = set()
    q = Queue(); q.put(curr)
    while not q.empty():
        curr = q.get(); cluster.add(curr)
        for n in g[curr]:
            if n in explore:
                q.put(n); explore.remove(n)
    if len(cluster) == 1:
        print('%s\t-1' % cluster.pop())
    else:
        CLUST += 1
        for n in cluster:
            print('%s\t%d' % (n,CLUST))
