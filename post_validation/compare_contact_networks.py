#! /usr/bin/env python3
'''
Compare a given simulated contact network against a given realistic reference
contact network.
'''
from common import avg,degrees
from numpy import std
from os.path import isfile
from scipy.stats import ks_2samp
from subprocess import check_output
import argparse

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', '--ref', required=True, type=str, help="Reference Contact Network")
parser.add_argument('-s', '--sim', required=True, type=str, help="Simulated Contact Network")
args,unknown = parser.parse_known_args()
assert isfile(args.ref), "ERROR: Invalid file: %s" % args.ref
assert isfile(args.sim), "ERROR: Invalid file: %s" % args.sim

# load data from contact networks
ref_degrees = degrees(open(args.ref))
sim_degrees = degrees(open(args.sim))

# perform analyses
print("Analysis\tReference Contact Network\tSimulated Contact Network\tTest Statistic\tp-value")
print("Average Degree\t%g\t%g\tNA\tNA" % (avg(ref_degrees),avg(sim_degrees)))
print("Standard Deviation Degree\t%g\t%g\tNA\tNA" % (std(ref_degrees),std(sim_degrees)))
print("Kolmogorov-Smirnov Test Degree\tNA\tNA\t%g\t%g" % ks_2samp(ref_degrees,sim_degrees))