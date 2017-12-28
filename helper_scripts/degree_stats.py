#!/usr/bin/env python3
'''
Compute useful statistics of the degrees of nodes in a given FAVITES-format
contact network or transmission network.
'''
MALFORMED = "Malformed file (must be in FAVITES format)"

# compute median of sorted list
def med(l):
    if len(l) % 2 == 0:
        return (l[int(len(l)/2)]+l[int(len(l)/2)-1])/2.
    else:
        return l[int(len(l)/2)]

# compute stats of list of numbers (len, sum, avg, var, std, min, q1, med, q3, max)
def stats(l_orig):
    l = sorted(l_orig)
    l_sum = 0.; l_sum_squares = 0.
    for e in l:
        l_sum += e; l_sum_squares += (e*e)
    l_avg = l_sum/len(l)
    l_var = (l_sum_squares/len(l)) - (l_avg*l_avg)
    l_std = l_var**0.5
    l_min = l[0]
    l_max = l[-1]
    l_q1 = med(l[:int((len(l)/2))])
    l_med = med(l)
    if len(l) % 2 == 0:
        l_q3 = med(l[int(len(l)/2):])
    else:
        l_q3 = med(l[:int((len(l)/2))+1])
    return len(l),l_sum,l_avg,l_var,l_std,l_min,l_q1,l_med,l_q3,l_max

if __name__ == "__main__":
    # parse args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), help="Contact or Transmission Network File")
    args,unknown = parser.parse_known_args()

    # parse contact/transmission network
    transmission = None; outdegree = {}; indegree = {}
    for line in args.input:
        l = line.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        parts = l.split('\t')
        assert len(parts) != 0, MALFORMED
        if transmission is None:
            transmission = {True:False,False:True}[parts[0] in {'NODE','EDGE'}]
        if transmission:
            assert len(parts) == 3, MALFORMED
            if parts[0] not in outdegree:
                outdegree[parts[0]] = 0
            outdegree[parts[0]] += 1
        else:
            assert parts[0] in {'NODE','EDGE'}, MALFORMED
            if parts[0] == 'NODE':
                assert len(parts) == 3, MALFORMED
                assert parts[1] not in outdegree, "Duplicate node: %s" % parts[1]
                outdegree[parts[1]] = 0; indegree[parts[1]] = 0
            elif parts[0] == 'EDGE':
                assert len(parts) == 5, MALFORMED
                assert parts[1] in outdegree, "Node %s not specified before edges" % parts[1]
                assert parts[2] in outdegree, "Node %s not specified before edges" % parts[2]
                assert parts[4] in {'d','u'}, MALFORMED
                outdegree[parts[1]] += 1; indegree[parts[2]] += 1
                if parts[4] == 'u':
                    outdegree[parts[2]] += 1; indegree[parts[1]] += 1

    # compute degree statistics
    outdegrees = [outdegree[n] for n in outdegree]; indegrees = [indegree[n] for n in indegree]
    print("### Out-Degree Stats ###\nLength:\t%d\nSum:\t%d\nAvg:\t%f\nVar:\t%f\nStdev:\t%f\nMin:\t%f\nQ1:\t%f\nMed:\t%f\nQ3:\t%f\nMax:\t%f" % stats(outdegrees))
    if not transmission:
        print()
        print("### In-Degree Stats ###\nLength:\t%d\nSum:\t%d\nAvg:\t%f\nVar:\t%f\nStdev:\t%f\nMin:\t%f\nQ1:\t%f\nMed:\t%f\nQ3:\t%f\nMax:\t%f" % stats(indegrees))