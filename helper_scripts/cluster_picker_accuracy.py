#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--clusterpicker_list', required=True, type=str, help="ClusterPicker list.txt file")
parser.add_argument('-t', '--trans', required=True, type=str, help="FAVITES transmission network (.txt)")
args = parser.parse_args()
for name in [e.strip() for e in args.trans.split('/')]:
    if 'CLUSTERS_' in name:
        break
true_clusters = {}
true_node_to_cluster = {}
for line in open(args.trans):
    u,v,t = line.split(); u,v,t = u.strip(),v.strip(),t.strip()
    if u == 'None':
        true_clusters[v] = {v}
        true_node_to_cluster[v] = v
    else:
        c = true_node_to_cluster[u]
        true_clusters[c].add(v)
        true_node_to_cluster[v] = c
cp_clusters = {'-1':set()} # -1 implies no cluster
cp_node_to_cluster = {}
for line in open(args.clusterpicker_list):
    if 'SequenceName' in line:
        continue
    n,c = line.split(); c = c.strip(); n = n.split('_')[1][1:]
    cp_node_to_cluster[n] = c
    if c == '-1':
        continue
    if c not in cp_clusters:
        cp_clusters[c] = {n}
    else:
        cp_clusters[c].add(n)
FP = 0
FN = 0
TP = 0
TN = 0
for u in cp_node_to_cluster:
    u_true = true_node_to_cluster[u]
    u_cp = cp_node_to_cluster[u]
    for v in cp_node_to_cluster:
        if u == v:
            continue
        v_true = true_node_to_cluster[v]
        v_cp = cp_node_to_cluster[v]
        if u_true == v_true: # actually a positive
            if u_cp != '-1' and u_cp == v_cp: # true positive
                TP += 1
            else:
                FN += 1
        else: # actually a negative
            if u_cp != '-1' and u_cp == v_cp: # false positive
                FP += 1
            else:
                TN += 1
print("TP: %d\nTN: %d\nFP: %d\nFN: %d" % (TP,TN,FP,FN))
if FP != 0:
    print("Precision: %f" % (TP/(TP+FP)))
else:
    print("Precision: 1")
if FN != 0:
    print("Recall: %f" % (TP/(TP+FN)))
else:
    print("Recall: 1")
