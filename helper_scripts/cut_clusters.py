#!/usr/bin/env python3
'''
Given a true phylogenetic tree and a distance, cut the tree at the given
distance and output the resulting clusters. This is intended to be used to
create "true" clusters from a true tree. Note that the given distance can either
be distance from the root (-m r) or distance from the lowest leaf (-m l).
'''

def cut_from_root(t,d,o):
    cluster_num = 1
    t.seed_node.root_dist = 0 # this will keep track of each node's distance from the root
    from queue import Queue
    q = Queue(); q.put(t.seed_node)
    while not q.empty():
        n = q.get()
        if n.is_leaf():
            o.write('%s\t%d\n' % (str(n.taxon)[1:-1],-1))
        elif n.root_dist >= d:
            for l in n.leaf_iter():
                o.write('%s\t%d\n' % (str(l.taxon)[1:-1],cluster_num))
            cluster_num += 1
        else:
            for c in n.child_node_iter():
                c.root_dist = n.root_dist + c.edge_length; q.put(c)

def cut_from_longest_leaf(t,d,o):
    longest = (None,float('-inf'))
    for n in t.preorder_node_iter():
        if n.parent_node is None:
            n.root_dist = 0
        else:
            n.root_dist = n.parent_node.root_dist + n.edge_length
        if n.is_leaf() and n.root_dist > longest[1]:
            longest = (n,n.root_dist)
    cut_from_root(t,longest[1]-d,o)

CUT = {'r':cut_from_root, 'l':cut_from_longest_leaf}
if __name__ == "__main__":
    # parse args
    from sys import stdout; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tree', required=True, type=argparse.FileType('r'), help="Tree File")
    parser.add_argument('-s', '--schema', required=False, type=str, default="newick", help="Tree File Schema")
    parser.add_argument('-m', '--mode', required=True, type=str, help="Mode (r for root, l for lowest leaf)")
    parser.add_argument('-d', '--distance', required=True, type=float, help="Distance")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output File")
    args = parser.parse_args()
    assert args.mode.lower() in CUT, "Invalid mode: %s" % args.mode

    # load tree
    try:
        from dendropy import Tree
    except:
        assert False, "Error loading DendroPy. Install with: pip3 install dendropy"
    t = Tree.get(file=args.tree, schema=args.schema.strip())

    # perform tree cutting custer generation
    args.output.write('SequenceName\tClusterNumber\n')
    CUT[args.mode.lower()](t,args.distance,args.output)