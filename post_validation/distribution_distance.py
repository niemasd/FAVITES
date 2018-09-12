#! /usr/bin/env python3
'''
Compute a distance between two distributions given samples from each.
'''
from gzip import open as gopen
from os.path import isfile
from numpy import linspace
from scipy.stats import entropy,ks_2samp,gaussian_kde
import argparse

# Kolmogorov-Smirnov, returns (distance, p-value) tuple
def d_ks(p_vec, q_vec):
    return tuple(ks_2samp(p_vec,q_vec))

# Jensen-Shannon Divergence
def d_jsd(p_vec, q_vec, num_points):
    p_pdf = gaussian_kde(p_vec); q_pdf = gaussian_kde(q_vec)
    l = min(min(p_vec),min(q_vec)); r = max(max(p_vec),max(q_vec)); lin = linspace(l,r,num_points)
    p = p_pdf.pdf(lin); q = q_pdf.pdf(lin); m = (p+q)/2
    return (entropy(p,m,2) + entropy(q,m,2)) / 2

# Jensen-Shannon Metric (square root of Jensen-Shannon Divergence)
def d_jsm(p_vec, q_vec, num_points):
    return d_jsd(p_vec,q_vec,num_points)**0.5

DISTANCES = {
    'jsd': d_jsd,
    'jsm': d_jsm,
    'ks': d_ks,
}
NEED_NUM_POINTS = {'jsd','jsm'}

if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-1', '--dist1', required=True, type=str, help="File containing samples from distribution 1")
    parser.add_argument('-2', '--dist2', required=True, type=str, help="File containing samples from distribution 2")
    parser.add_argument('-d', '--distance', required=False, type=str, default='jsd', help="Distance (jsd = Jensen-Shannon Divergence, jsm = Jensen-Shannon Metric, ks = Kolmogorov-Smirnov")
    parser.add_argument('-n', '--num_points', required=False, type=int, default=100, help="Number of Points when Discretizing PDF (used in jsd, jsm)")
    args,unknown = parser.parse_known_args()
    assert isfile(args.dist1), "Invalid file: %s" % args.dist1
    assert isfile(args.dist2), "Invalid file: %s" % args.dist2
    assert args.distance.lower() in DISTANCES, "Invalid distance: %s" % args.distance
    assert args.num_points > 0, "num_points must be positive"

    # load datasets
    if args.dist1.lower().endswith('.gz'):
        p_vec = [float(l) for l in gopen(args.dist1).read().decode().strip().splitlines()]
    else:
        p_vec = [float(l) for l in open(args.dist1).read().strip().splitlines()]
    if args.dist2.lower().endswith('.gz'):
        q_vec = [float(l) for l in gopen(args.dist2).read().decode().strip().splitlines()]
    else:
        q_vec = [float(l) for l in open(args.dist2).read().strip().splitlines()]

    # compute distances
    if args.distance.lower() in NEED_NUM_POINTS:
        print(DISTANCES[args.distance.lower()](p_vec,q_vec,args.num_points))
    else:
        print(DISTANCES[args.distance.lower()](p_vec,q_vec))
