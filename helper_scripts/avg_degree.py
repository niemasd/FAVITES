#!/usr/bin/env python3
'''
Compute the average degree of nodes in a given FAVITES-format contact network.
'''
MALFORMED = "Malformed contact network file (must be in FAVITES format)"

if __name__ == "__main__":
    # parse args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--contact_network', required=True, type=argparse.FileType('r'), help="Contact Network File")
    args = parser.parse_args()

    # compute average degree
    outgoing = {}; incoming = {}
    for line in args.contact_network:
        l = line.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        parts = l.split('\t')
        assert len(parts) != 0 and parts[0] in {'NODE','EDGE'}, MALFORMED
        if parts[0] == 'NODE':
            assert len(parts) == 3, MALFORMED
            assert parts[1] not in outgoing, "Duplicate node: %s" % parts[1]
            outgoing[parts[1]] = set(); incoming[parts[1]] = set()
        elif parts[0] == 'EDGE':
            assert len(parts) == 5, MALFORMED
            assert parts[1] in outgoing, "Node %s not specified before edges" % parts[1]
            assert parts[2] in outgoing, "Node %s not specified before edges" % parts[2]
            assert parts[4] in {'d','u'}, MALFORMED
            outgoing[parts[1]].add(parts[2]); incoming[parts[2]].add(parts[1])
            if parts[4] == 'u':
                outgoing[parts[2]].add(parts[1]); incoming[parts[1]].add(parts[2])
    print("Average In-Degree:  %f" % (float(sum([len(incoming[n]) for n in incoming]))/len(incoming)))
    print("Average Out-Degree: %f" % (float(sum([len(outgoing[n]) for n in outgoing]))/len(outgoing)))