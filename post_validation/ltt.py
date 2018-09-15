#! /usr/bin/env python3
'''
Create an LTT plot from one or more Newick trees.
'''
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from os.path import isfile
from subprocess import check_output
from treeswift import read_tree_newick
import argparse
import matplotlib.pyplot as plt

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('trees', metavar='N', type=str, nargs='+', help="Newick Trees")
parser.add_argument('-p', '--present_day', required=False, type=float, default=None, nargs='+', help="Present Day (furthest time from root)")
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-xmin', '--xmin', required=False, type=float, default=None, help="X-Axis Minimum")
parser.add_argument('-xmax', '--xmax', required=False, type=float, default=None, help="X-Axis Maximum")
parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
args,unknown = parser.parse_known_args()
for t in args.trees:
    assert isfile(t), "Invalid file: %s" % t
if args.present_day is None:
    args.present_day = [None]*len(args.trees)
assert len(args.present_day) == len(args.trees), "Number of present day times must equal number of trees"
colors = plt.cm.tab10(range(len(args.trees)))
handles = [Patch(color=colors[i],label=args.trees[i]) for i in range(len(colors))]

# plot LTTs
xmin = float('inf'); xmax = float('-inf')
ymin = float('inf'); ymax = float('-inf')
for i in range(len(args.trees)):
    ltt = read_tree_newick(args.trees[i]).ltt(present_day=args.present_day[i], color=colors[i], show_plot=False)
    xmin = min(xmin,min(ltt.keys())); xmax = max(xmax,max(ltt.keys()))
    ymin = min(ymin,min(ltt.values())); ymax = max(ymax,max(ltt.values())*1.1)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)
if args.xmin is not None:
    xmin = args.xmin
if args.xmax is not None:
    xmax = args.xmax
if args.ymin is not None:
    ymin = args.ymin
if args.ymax is not None:
    ymax = args.ymax
plt.xlim(xmin=xmin,xmax=xmax); plt.ylim(ymin=ymin,ymax=ymax)
legend = plt.legend(handles=handles)
plt.show()
