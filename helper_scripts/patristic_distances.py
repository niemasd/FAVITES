#!/usr/bin/env python3
'''
Compute the pairwise distances between leaves of a given phylogenetic tree and
output as a CSV.
'''

if __name__ == "__main__":
    # parse args
    from sys import stdout; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tree', required=True, type=argparse.FileType('r'), help="Tree File")
    parser.add_argument('-s', '--schema', required=False, type=str, default="newick", help="Tree File Schema")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output File")
    parser.add_argument('-d', '--self_distance', required=False, type=str, default="0", help="String to Report Self-Distance (diagonal)")
    args,unknown = parser.parse_known_args()

    # load tree and compute distances
    try:
        from dendropy import Tree
    except:
        assert False, "Error loading DendroPy. Install with: pip3 install dendropy"
    t = Tree.get(file=args.tree, schema=args.schema.strip())
    d = t.phylogenetic_distance_matrix()
    args.output.write(",%s\n" % ','.join([str(e)[1:-1] for e in t.taxon_namespace]))
    for t1 in t.taxon_namespace:
        args.output.write("%s,%s\n" % (str(t1)[1:-1], ','.join([str(d(t1,t2)) if t1 != t2 else args.self_distance for t2 in t.taxon_namespace])))
