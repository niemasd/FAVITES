#!/usr/bin/env python3
'''
Score a given ClusterPicker-format clustering against the known truth clustering (from the transmission network).
    * AMI = Adjusted Mutual Information
    * ARI = Adjusted Rand Index
    * COM = Completeness Score
    * FMI = Fowlkes-Mallows Index
    * HCV = Compute Homogenity, Completeness, and V-Measure together
    * HOM = Homogeneity Score
    * MI = Mutual Information
    * NMI = Normalized Mutual Information
    * VM = V-Measure
'''
from sklearn.metrics.cluster import *
METRICS = {'AMI':adjusted_mutual_info_score, 'ARI':adjusted_rand_score, 'COM':completeness_score, 'FMI':fowlkes_mallows_score, 'HCV':homogeneity_completeness_v_measure, 'HOM':homogeneity_score, 'MI':mutual_info_score, 'NMI':normalized_mutual_info_score, 'VM':v_measure_score}
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
            true_node_to_cluster[v] = true_node_to_cluster[u]
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
    cp_clusters_list = []
    for i in range(len(num_to_name)):
        try:
            cp_clusters_list.append(cp_node_to_cluster[num_to_name[i]])
        except KeyError: # tn93 doesn't output singletons
            cp_clusters_list.append(c); c += 1

    # compute and output score
    if args.metric == 'HCV':
        h,c,v = METRICS[args.metric](true_clusters_list,cp_clusters_list)
        print("HOM: %f" % h); print("COM: %f" % c); print("VM: %f" % v)
    else:
        print("%s: %f" % (args.metric, METRICS[args.metric](true_clusters_list,cp_clusters_list)))
