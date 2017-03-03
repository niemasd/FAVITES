#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Dual Birth model
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
import queue as Q

class NodeEvolution_DualBirth(NodeEvolution):
    def init():
        global exponential
        from numpy.random import exponential
        GC.dualbirth_beta = 1/(float(GC.rate_B))
        GC.dualbirth_betaP = 1/(float(GC.rate_A))

    def evolve_to_current_time(node, finalize=False):
        TreeNode = MF.modules['TreeNode']
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            node.remove_virus(virus)

            # if this is the first time this node is evolving, it must start active
            if not hasattr(virus,'active'):
                virus.active = True

            # can't assume virus immediately starts replicating
            extra_time = 0
            if virus.active:
                extra_time = exponential(scale=GC.dualbirth_betaP)
            else:
                extra_time = exponential(scale=GC.dualbirth_beta)
            virus.set_time(virus.get_time() + extra_time)

            # initialize simulation
            done = []
            pq = Q.PriorityQueue()
            if virus.get_time() < GC.time:
                pq.put((virus.get_time(), virus))
            else:
                done.append(virus)


            # perform simulation
            while not pq.empty():
                # get next node
                currTime, currNode = pq.get()
                currNode.active = True

                # self propagation
                leftLength = exponential(scale=GC.dualbirth_betaP)
                leftChild = TreeNode(time=currNode.get_time()+leftLength, contact_network_node=node)
                leftChild.active = True
                currNode.add_child(leftChild)
                if leftChild.get_time() < GC.time:
                    pq.put((leftChild.get_time(), leftChild))
                else:
                    done.append(leftChild)

                # newly created inactive child
                rightLength = exponential(scale=GC.dualbirth_beta)
                rightChild = TreeNode(time=currNode.get_time()+rightLength, contact_network_node=node)
                rightChild.active = False
                currNode.add_child(rightChild)
                if rightChild.get_time() < GC.time:
                    pq.put((rightChild.get_time(), rightChild))
                else:
                    done.append(rightChild)

            # truncate final edges to be same as shortest leaf and add back to node
            for leaf in done:
                leaf.set_time(GC.time)
                node.add_virus(leaf)