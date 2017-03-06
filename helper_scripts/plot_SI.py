#! /usr/bin/env python3
'''
Given a transmission network file (FAVITES format) generated under the SI model,
plot Susceptible and Infected vs. time.
'''
import sys,seaborn
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: Incorrect number of arguments")
        print("USAGE: python plot_SI.py <transmission_network_file>")
        exit(-1)
    tn = [line.strip().split('\t') for line in open(sys.argv[1]).read().strip().splitlines()]
    nodes = set()
    infected = set()
    for t in tn:
        t[2] = float(t[2])
        nodes.add(t[0])
        nodes.add(t[1])
        infected.add(t[1])
    seeds = len(nodes) - len(infected)
    time = [0]
    S = [len(infected)]
    I = [seeds]
    for u,v,t in tn:
        time.append(t)
        S.append(S[-1]-1)
        I.append(I[-1]+1)
    plt.plot(time,S,'bo',label="Susceptible")
    plt.plot(time,I,'ro',label="Infected")
    plt.title("SI Model Simulation")
    plt.ylabel("Number of Individuals")
    plt.xlabel("Time")
    plt.legend()
    plt.show()