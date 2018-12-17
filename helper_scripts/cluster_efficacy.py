#!/usr/bin/env python3
'''
Compute clustering efficacy (average number of individuals infected by
user-selected individuals between from_time and to_time).
'''
from gzip import open as gopen
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--individuals', required=False, type=str, default='stdin', help="Individuals (one per line)")
parser.add_argument('-tn', '--transmissions', required=True, type=str, help="Transmission Network (FAVITES format)")
parser.add_argument('-t', '--from_time', required=True, type=float, help="From Time")
parser.add_argument('-tt', '--to_time', required=False, type=float, default=float('inf'), help="To Time")

args = parser.parse_args()
assert args.to_time > args.from_time, "To Time must be larger than From Time"
if args.individuals == 'stdin':
    from sys import stdin; args.individuals = stdin.read().strip().splitlines()
elif args.individuals.endswith('.gz'):
    args.individuals = gopen(args.individuals).read().strip().decode().splitlines()
else:
    args.individuals = open(args.individuals).read().strip().splitlines()
if args.transmissions.endswith('.gz'):
    args.transmissions = gopen(args.transmissions).read().strip().decode().splitlines()
else:
    args.transmissions = open(args.transmissions).read().strip().splitlines()

# load FAVITES transmission network
trans = []; nodes = set()
for line in args.transmissions:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    try:
        u,v,t = l.split(); t = float(t)
    except:
        raise RuntimeError("Invalid transmission network")
    if u not in nodes:
        nodes.add(u)
    if v not in nodes:
        nodes.add(v)
    trans.append((u,v,t))

# load user's individuals
user_individuals = set()
for line in args.individuals:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    assert l in nodes, "Individual not in transmission network: %s"%l
    user_individuals.add(l)

# compute average number infected
avg = 0.
for u,v,t in trans:
    if t >= args.from_time and t <= args.to_time and u in user_individuals:
        avg += 1
avg /= len(user_individuals)
print(avg)
