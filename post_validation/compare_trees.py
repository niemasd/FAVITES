#! /usr/bin/env python3
'''
Niema Moshiri 2017

Compare a given simulated tree against a given realistic reference tree.
'''
from common import avg
from numpy import std
from os.path import isfile
from scipy.stats import ks_2samp
from subprocess import check_output
import argparse

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', '--ref', required=True, type=str, help="Reference Tree")
parser.add_argument('-s', '--sim', required=True, type=str, help="Simulated Tree")
parser.add_argument('-n', '--nw_distance', required=False, type=str, default='nw_distance', help="Path to nw_distance")
args = parser.parse_args()
assert isfile(args.ref), "ERROR: Invalid file: %s" % args.ref
assert isfile(args.sim), "ERROR: Invalid file: %s" % args.sim

# load data from trees
ref_int_bl = [float(i) for i in check_output([args.nw_distance, '-mp', '-si', args.ref]).split()]
ref_pen_bl = [float(i) for i in check_output([args.nw_distance, '-mp', '-sf', args.ref]).split()]
ref_tot_bl = ref_int_bl + ref_pen_bl
sim_int_bl = [float(i) for i in check_output([args.nw_distance, '-mp', '-si', args.sim]).split()]
sim_pen_bl = [float(i) for i in check_output([args.nw_distance, '-mp', '-sf', args.sim]).split()]
sim_tot_bl = sim_int_bl + sim_pen_bl

# perform analyses
print("Analysis\tReference Tree\tSimulated Tree\tTest Statistic\tp-value")
print("Average Branch Length\t%g\t%g\tNA\tNA" % (avg(ref_tot_bl),avg(sim_tot_bl)))
print("Standard Deviation Branch Length\t%g\t%g\tNA\tNA" % (std(ref_tot_bl),std(sim_tot_bl)))
print("Kolmogorov-Smirnov Test Branch Length\tNA\tNA\t%g\t%g" % ks_2samp(ref_tot_bl,sim_tot_bl))
print("Average Internal Branch Length\t%g\t%g\tNA\tNA" % (avg(ref_int_bl),avg(sim_int_bl)))
print("Standard Deviation Internal Branch Length\t%g\t%g\tNA\tNA" % (std(ref_int_bl),std(sim_int_bl)))
print("Kolmogorov-Smirnov Test Internal Branch Length\tNA\tNA\t%g\t%g" % ks_2samp(ref_int_bl,sim_int_bl))
print("Average Terminal Branch Length\t%g\t%g\tNA\tNA" % (avg(ref_pen_bl),avg(sim_pen_bl)))
print("Standard Deviation Terminal Branch Length\t%g\t%g\tNA\tNA" % (std(ref_pen_bl),std(sim_pen_bl)))
print("Kolmogorov-Smirnov Test Terminal Branch Length\tNA\tNA\t%g\t%g" % ks_2samp(ref_pen_bl,sim_pen_bl))
