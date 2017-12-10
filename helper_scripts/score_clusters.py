#!/usr/bin/env python3
'''
Score a given ClusterPicker-format clustering against the known truth clustering (from the transmission network).
'''
from sklearn.metrics.cluster import adjusted_mutual_info_score,adjusted_rand_score
METRICS = {'AMI':adjusted_mutual_info_score, 'AR':adjusted_rand_score}
if __name__ == "__main__":
    # parse args
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--clusterpicker_list', required=True, type=argparse.FileType('r'), help="ClusterPicker list.txt file")
    parser.add_argument('-t', '--trans', required=True, type=argparse.FileType('r'), help="FAVITES transmission network (.txt)")
    parser.add_argument('-m', '--metric', required=True, type=str, help="Scoring Method (options: %s)" % ', '.join(sorted(METRICS.keys())))
    args = parser.parse_args()
    args.metric = args.metric.strip().upper()
    assert args.metric in METRICS, "ERROR: Invalid metric: %s" % args.metric

    # load true transmission network
    name_to_num = {}
    num_to_name = []
    true_node_to_cluster = {}
    for line in args.trans:
        u,v,t = line.split(); u,v,t = u.strip(),v.strip(),t.strip()
        if v not in name_to_num:
            name_to_num[v] = len(name_to_num)
            num_to_name.append(v)
        if u == 'None' or u[0] == '-': # handle negative PANGEA sources
            true_node_to_cluster[v] = name_to_num[v]
        else:
            true_node_to_cluster[v] = name_to_num[u]
    true_clusters_list = [true_node_to_cluster[num_to_name[i]] for i in range(len(num_to_name))]

    # load inferred transmission clusters
    cp_node_to_cluster = {}
    for line in args.clusterpicker_list:
        if 'SequenceName' in line:
            continue
        n,c = line.split(); c = c.strip(); n = n.split('|')[1]
        cp_node_to_cluster[n] = int(c)
    c = max(cp_node_to_cluster.values())
    if c == -1:
        c = 1
    else:
        c += 1
    for n in cp_node_to_cluster:
        if cp_node_to_cluster[n] == -1:
            cp_node_to_cluster[n] = c; c += 1
    cp_clusters_list = [cp_node_to_cluster[num_to_name[i]] for i in range(len(num_to_name))]

    # compute and output score
    print("%s: %f" % (args.metric, METRICS[args.metric](true_clusters_list,cp_clusters_list)))
