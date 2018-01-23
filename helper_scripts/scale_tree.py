#!/usr/bin/env python3
'''
Scale the branches of a given Newick tree.
* Constant: Scale tree by multiplying all branches by a constant n: scale_tree.py -t TREE [-o OUTPUT] -m c CONSTANT
* Exponential: Scale tree by multiplying each branch by a multiplier sampled from an exponential r.v.: scale_tree.py -t TREE [-o OUTPUT] -m e SCALE
* Gamma: Scale tree by multiplying each branch by a multiplier sampled from a gamma r.v.: scale_tree.py -t TREE [-o OUTPUT] -m g SHAPE SCALE
* Log-Normal: Scale tree by multiplying each branch by a multiplier sampled from a log-normal r.v.: scale_tree.py -t TREE [-o OUTPUT] -m ln MU SIGMA
'''

# scale branches by a constant
def scale_constant(t,c):
    for e in t.preorder_edge_iter():
        if e.length is not None:
           e.length *= c

# scale branches by sampling multiplier from exponential
def scale_exponential(t,s):
    try:
        from numpy.random import exponential
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.preorder_edge_iter():
        if e.length is not None:
            e.length *= exponential(scale=s)

# scale branches by sampling multipler from gamma
def scale_gamma(t,shape,scale):
    try:
        from numpy.random import gamma
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.preorder_edge_iter():
        if e.length is not None:
            e.length *= gamma(shape=shape,scale=scale)

# scale branches by sampling multipler from log-normal
def scale_lognormal(t,mu,sigma):
    try:
        from numpy.random import lognormal
    except:
        assert False, "Error loading NumPy. Install with: pip3 install numpy"
    for e in t.preorder_edge_iter():
        if e.length is not None:
            e.length *= lognormal(mean=mu,sigma=sigma)

# main function
MODES = ['(C)onstant', '(E)xponential', '(G)amma', '(L)og-(N)ormal']
if __name__ == "__main__":
    # parse args
    from sys import stdout; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tree', required=True, type=argparse.FileType('r'), help="Tree File")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output File")
    parser.add_argument('-m', '--mode', required=True, type=str, help="Mode: %s" % ', '.join(MODES))
    parser.add_argument('parameters', metavar='p', type=float, nargs='*', help="Mode Parameters")
    args,unknown = parser.parse_known_args()

    # load tree and compute distances
    try:
        from dendropy import Tree
    except:
        assert False, "Error loading DendroPy. Install with: pip3 install dendropy"
    t = Tree.get(file=args.tree, schema='newick')
    m = args.mode.lower()
    if m == 'c':
        assert len(args.parameters) == 1, "Constant Mode Usage: scale_tree.py -t TREE [-o OUTPUT] -m c CONSTANT"
        scale_constant(t,args.parameters[0])
    elif m == 'e':
        assert len(args.parameters) == 1, "Exponential Mode Usage: scale_tree.py -t TREE [-o OUTPUT] -m e SCALE"
        scale_exponential(t,args.parameters[0])
    elif m == 'g':
        assert len(args.parameters) == 2, "Gamma Mode Usage: scale_tree.py -t TREE [-o OUTPUT] -m g SHAPE SCALE"
        scale_gamma(t,args.parameters[0],args.parameters[1])
    elif m == 'ln':
        assert len(args.parameters) == 2, "Log-Normal Mode Usage: scale_tree.py -t TREE [-o OUTPUT] -m ln MU SIGMA"
        scale_lognormal(t,args.parameters[0],args.parameters[1])
    else:
        assert False, "Invalid mode. Options: %s" % ', '.join(MODES)
    args.output.write("%s;\n" % str(t))