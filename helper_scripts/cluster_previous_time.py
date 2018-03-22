#!/usr/bin/env python3
'''
Given a clustering (in the Cluster Picker format) from the simulation end time,
a FAVITES-format transmission network, and an end time, remove individuals who
were not infected at the given time and output the resulting clusters.
'''
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--clustering', required=True, type=argparse.FileType('r'), help="Clustering (Cluster Picker format)")
parser.add_argument('-tn', '--transmissions', required=True, type=argparse.FileType('r'), help="Transmission Network (FAVITES format)")
parser.add_argument('-t', '--time', required=True, type=float, help="End Time")
parser.add_argument('-o', '--output', required=False, default='stdout', help="Output File")
args = parser.parse_args()
assert args.time > 0, "End time must be positive"
if args.output == 'stdout':
    from sys import stdout; args.output = stdout
else:
    args.output = open(args.output,'w')

# load FAVITES transmission network
infection_windows = {}
for l in args.transmissions:
    try:
        u,v,t = l.split(); t = float(t)
    except:
        raise RuntimeError("Invalid transmission network")
    if u not in infection_windows:
        infection_windows[u] = []
    if v not in infection_windows:
        infection_windows[v] = []
    if u != v and (len(infection_windows[v]) == 0 or infection_windows[v][-1][1] is not None):
        infection_windows[v].append([t,None])
    else:
        assert len(infection_windows[v]) != 0 and infection_windows[v][-1][1] is None, "Invalid transmission network: recovering uninfected individual"
        infection_windows[v][-1][1] = t
for v in infection_windows:
    if len(infection_windows[v]) != 0 and infection_windows[v][-1][1] is None:
        infection_windows[v][-1][1] = float('inf')

# determine which individuals need to be removed
to_remove = set()
for v in infection_windows:
    if len(infection_windows[v]) == 0:
        continue
    remove = True
    for start,end in infection_windows[v]:
        if start <= args.time and end >= args.time:
            remove = False; break
    if remove:
        to_remove.add(v)

# output filtered clusters
for line in args.clustering:
    l = line.strip()
    if l.startswith('Sequence'):
        args.output.write("%s\n"%l); continue
    try:
        n,c = l.split(); n = n.split('|')[1]
    except:
        raise RuntimeError("Invalid clustering file")
    if n not in to_remove:
        args.output.write("%s\n"%l)
