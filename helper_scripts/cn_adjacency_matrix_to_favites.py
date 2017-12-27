#!/usr/bin/env python3
'''
Convert a given contact network binary adjacency matrix to the FAVITES format
'''
from sys import stdout

if __name__ == "__main__":
    # parse args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), help="Contact Network File (binary adjacency matrix)")
    parser.add_argument('-o', '--output', required=False, default=stdout, type=argparse.FileType('w'), help="Output File")
    parser.add_argument('-d', '--delim', required=False, default=None, type=str, help="Column Delimiter")
    args,unknown = parser.parse_known_args()

    # parse contact network
    g = {}
    lines = [i.strip() for i in args.input if len(i.strip()) > 0 and i.strip()[0] != '#']
    out = ["NODE\t%d\t." % i for i in range(len(lines))]
    for i in range(len(lines)):
        if args.delim:
            parts = lines[i].split(args.delim)
        else:
            parts = lines[i]
        assert len(parts) == len(lines), "The number of rows and columns must be the same"
        for j in range(len(parts)):
            if parts[j] == '1':
                out.append("EDGE\t%s\t%s\t.\t%s" % (str(i),str(j),'d'))
            else:
                assert parts[j] == '0', "Invalid matrix element. Must only contain 1s and 0s"
    args.output.write('\n'.join(out)); args.output.close()