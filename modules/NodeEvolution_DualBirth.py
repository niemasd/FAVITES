#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Dual Birth model
'''
from NodeEvolution import NodeEvolution # abstract NodeEvolution class
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from numpy.random import exponential
import queue as Q

class NodeEvolution_DualBirth(NodeEvolution):
    def evolve_to_current_time(node, finalize=False):
        TreeNode = MF.modules['TreeNode']
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            node.remove_virus(virus)

            # numpy uses scale parameters for exponential (beta = 1/lambda)
            beta = 1/(float(GC.rate_B))
            betaP = 1/(float(GC.rate_A))

            # initialize simulation
            pq = Q.PriorityQueue()
            pq.put((virus.get_time(), virus))
            currNode = virus
            currTime = virus.get_time()

            # perform simulation
            while currTime < GC.time:
                # self propagation
                leftLength = exponential(scale=betaP)
                leftChild = TreeNode(time=currNode.get_time()+leftLength, contact_network_node=node)
                currNode.add_child(leftChild)
                pq.put((leftChild.get_time(), leftChild))

                # newly created inactive child
                rightLength = exponential(scale=beta)
                rightChild = TreeNode(time=currNode.get_time()+rightLength, contact_network_node=node)
                currNode.add_child(rightChild)
                pq.put((rightChild.get_time(), rightChild))

                # get next node
                currTime, currNode = pq.get()

            # get leaves from pq
            leaves = [currNode]
            while not pq.empty():
                leaves.append(pq.get()[1])

            # truncate final edges to be same as shortest leaf and add back to node
            for leaf in leaves:
                leaf.set_time(GC.time)
                node.add_virus(leaf)