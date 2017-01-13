#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Dual Birth model
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from numpy.random import exponential
import queue as Q

class NodeEvolution_DualBirth(NodeEvolution):
    def init():
        GC.dualbirth_beta = 1/(float(GC.rate_B))
        GC.dualbirth_betaP = 1/(float(GC.rate_A))

    def evolve_to_current_time(node, finalize=False):
        TreeNode = MF.modules['TreeNode']
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            node.remove_virus(virus)

            # initialize simulation
            pq = Q.PriorityQueue()
            pq.put((virus.get_time(), virus))


            # perform simulation
            done = []
            while not pq.empty() > 0:
                # get next node
                currTime, currNode = pq.get()

                # self propagation
                leftLength = exponential(scale=GC.dualbirth_betaP)
                leftChild = TreeNode(time=currNode.get_time()+leftLength, contact_network_node=node)
                currNode.add_child(leftChild)
                if leftChild.get_time() < GC.time:
                    pq.put((leftChild.get_time(), leftChild))
                else:
                    done.append(leftChild)

                # newly created inactive child
                rightLength = exponential(scale=GC.dualbirth_beta)
                rightChild = TreeNode(time=currNode.get_time()+rightLength, contact_network_node=node)
                currNode.add_child(rightChild)
                if rightChild.get_time() < GC.time:
                    pq.put((rightChild.get_time(), rightChild))
                else:
                    done.append(rightChild)

            # truncate final edges to be same as shortest leaf and add back to node
            for leaf in done:
                leaf.set_time(GC.time)
                node.add_virus(leaf)