#!/usr/bin/env python3
'''
Label the internal nodes of a given tree with the individual inside which the corresponding ancestral node existed.
'''
TREESWIFT_IMPORT_ERROR = "Error importing TreeSwift. Install with: pip3 install treeswift"
MUTATION_FILE_ERROR = "If you specify an input mutation tree file, you must also specify an output mutation tree file (and vice-versa)"
try:
    from treeswift import read_tree_newick
except:
    raise ImportError(TREESWIFT_IMPORT_ERROR)

# main function
if __name__ == "__main__":
    # parse args
    from sys import stdin,stdout; from gzip import open as gopen; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-tn', '--transmission_network', required=True, type=str, help="Input Transmission Network File")
    parser.add_argument('-tt', '--tree_time', required=True, type=str, help="Input Time Tree File")
    parser.add_argument('-tm', '--tree_mutation', required=False, type=str, default=None, help="Input Mutation Tree File")
    parser.add_argument('-ot', '--output_time', required=True, type=str, help="Output Labeled Time Tree File")
    parser.add_argument('-om', '--output_mutation', required=False, type=str, default=None, help="Output Mutation Tree File")
    args,unknown = parser.parse_known_args()
    if (args.tree_mutation is None and args.output_mutation is not None) or (args.tree_mutation is not None and args.output_mutation is None):
        raise ValueError(MUTATION_FILE_ERROR)
    tt = read_tree_newick(args.tree_time)
    tm = None
    if args.tree_mutation is not None:
        tm = read_tree_newick(args.tree_mutation)
    if args.transmission_network.lower().endswith('.gz'):
        tn = gopen(args.transmission_network)
    else:
        tn = open(args.transmission_network)
    if args.output_time.lower().endswith('.gz'):
        ot = gopen(args.output_time,'wb',9)
    else:
        ot = open(args.output_time,'w')
    if args.output_mutation is not None:
        if args.output_mutation.lower().endswith('.gz'):
            om = gopen(args.output_mutation,'wb',9)
        else:
            om = open(args.output_mutation,'w')

    # if mutation tree specified, map nodes from time tree to mutation tree
    tt2tm = None
    if tm is not None:
        tm_label2node = {l.label:l for l in tm.traverse_leaves()}
        tt2tm = {l:tm_label2node[l.label] for l in tt.traverse_leaves()}
        for l_tt in tt.traverse_leaves():
            c_tm = tt2tm[l_tt].parent
            for c_tt in l_tt.traverse_ancestors(include_self=False):
                if c_tt in tt2tm:
                    break
                tt2tm[c_tt] = c_tm; c_tm = c_tm.parent

    # read seeds and infection times from transmission network
    inf = {None:float('inf')}; seeds = set()
    for l in tn:
        if isinstance(l,bytes):
            u,v,t = l.decode().strip().split('\t')
        else:
            u,v,t = l.strip().split('\t')
        if u == 'None':
            seeds.add(v); inf[v] = float('-inf')
        elif v not in inf:
            inf[v] = float(t)

    # label internal nodes
    person = dict()
    for u in tt.traverse_postorder():
        if u.is_leaf():
            person[u] = u.label.split('|')[1]
        else:
            if sum(person[c] in seeds for c in u.children) > 1:
                person[u] = None
            else:
                person[u] = sorted((inf[person[c]],person[c]) for c in u.children)[0][1]
            if person[u] is not None:
                u.label = person[u]
            if tt2tm is not None:
                tt2tm[u].label = person[u]

    # output resulting tree(s)
    if args.output_time.lower().endswith('.gz'):
        ot.write(tt.newick().encode()); ot.write(b'\n'); ot.close()
    else:
        ot.write(tt.newick()); ot.write('\n'); ot.close()
    if args.output_mutation is not None:
        if args.output_mutation.lower().endswith('.gz'):
            om.write(tm.newick().encode()); om.write(b'\n'); om.close()
        else:
            om.write(tm.newick()); om.write('\n'); om.close()
