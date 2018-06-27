#!/usr/bin/env python3
'''
Scale the branches of a given Newick tree.
* Autocorrelated Exponential: Scale tree by multiplying each branch by a multiplier sampled from an exponential r.v. with rate equal to parent's multiplier: scale_tree.py [-t TREE] [-o OUTPUT] -m ae SCALE
* Constant: Scale tree by multiplying all branches by a constant n: scale_tree.py [-t TREE] [-o OUTPUT] -m c CONSTANT
* Exponential: Scale tree by multiplying each branch by a multiplier sampled from an exponential r.v.: scale_tree.py [-t TREE] [-o OUTPUT] -m e SCALE
* Gamma: Scale tree by multiplying each branch by a multiplier sampled from a gamma r.v.: scale_tree.py [-t TREE] [-o OUTPUT] -m g SHAPE SCALE
* Log-Normal: Scale tree by multiplying each branch by a multiplier sampled from a log-normal r.v.: scale_tree.py [-t TREE] [-o OUTPUT] -m ln MU SIGMA
'''

# scale branches by autocorrelated exponential
def scale_autocorrelated_exponential(t,s):
    try:
        from numpy.random import exponential
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.traverse_preorder():
        if e.is_root():
            e.rate = s
        else:
            e.rate = exponential(scale = 1./e.parent.rate)
        if e.edge_length is not None:
            e.edge_length *= e.rate

# scale branches by a constant
def scale_constant(t,c):
    for e in t.traverse_preorder():
        if e.edge_length is not None:
           e.edge_length *= c

# scale branches by sampling multiplier from exponential
def scale_exponential(t,s):
    try:
        from numpy.random import exponential
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.traverse_preorder():
        if e.edge_length is not None:
            e.edge_length *= exponential(scale=s)

# scale branches by sampling multipler from gamma
def scale_gamma(t,shape,scale):
    try:
        from numpy.random import gamma
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.traverse_preorder():
        if e.edge_length is not None:
            e.edge_length *= gamma(shape=shape,scale=scale)

# scale branches by sampling multipler from log-normal
def scale_lognormal(t,mu,sigma):
    try:
        from numpy.random import lognormal
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.traverse_preorder():
        if e.edge_length is not None:
            e.edge_length *= lognormal(mean=mu,sigma=sigma)

# main function
MODES = ['(C)onstant', '(E)xponential', '(G)amma', '(L)og-(N)ormal']
if __name__ == "__main__":
    # parse args
    from sys import stdin,stdout; from gzip import open as gopen; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Tree File")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-m', '--mode', required=True, type=str, help="Mode: %s" % ', '.join(MODES))
    parser.add_argument('parameters', metavar='p', type=float, nargs='*', help="Mode Parameters")
    args,unknown = parser.parse_known_args()
    if args.input == 'stdin':
        treestr = stdin.read()
    elif args.input.lower().endswith('.gz'):
        treestr = gopen(args.input).read().decode()
    else:
        treestr = open(args.input).read()
    if args.output == 'stdout':
        args.output = stdout
    else:
        args.output = open(args.output,'w')

    # load tree and compute distances
    try:
        from treeswift import read_tree_newick
    except:
        assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
    t = read_tree_newick(treestr)
    m = args.mode.lower()
    if m == 'ae':
        assert len(args.parameters) == 1, "Autocorrelated Exponential Mode Usage: scale_tree.py [-t TREE] [-o OUTPUT] -m ae SCALE"
        scale_autocorrelated_exponential(t,args.parameters[0])
    elif m == 'c':
        assert len(args.parameters) == 1, "Constant Mode Usage: scale_tree.py [-t TREE] [-o OUTPUT] -m c CONSTANT"
        scale_constant(t,args.parameters[0])
    elif m == 'e':
        assert len(args.parameters) == 1, "Exponential Mode Usage: scale_tree.py [-t TREE] [-o OUTPUT] -m e SCALE"
        scale_exponential(t,args.parameters[0])
    elif m == 'g':
        assert len(args.parameters) == 2, "Gamma Mode Usage: scale_tree.py [-t TREE] [-o OUTPUT] -m g SHAPE SCALE"
        scale_gamma(t,args.parameters[0],args.parameters[1])
    elif m == 'ln':
        assert len(args.parameters) == 2, "Log-Normal Mode Usage: scale_tree.py [-t TREE] [-o OUTPUT] -m ln MU SIGMA"
        scale_lognormal(t,args.parameters[0],args.parameters[1])
    else:
        assert False, "Invalid mode. Options: %s" % ', '.join(MODES)
    args.output.write("%s\n" % str(t)); args.output.close()