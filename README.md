#FAVITES - FrAmework for VIral Transmission and Evolution Simulation

Architecture
===
FILL THIS OUT

Requirements
===
To run FAVITES, you must use [Python 3](https://www.python.org/downloads/). Each
module implementation may have its own additional dependencies (see below). To
guarantee that your setup works with *all* module implementations, here is a
comprehensive list of dependencies across all current module implementations:
* [DendroPy](http://www.dendropy.org/) (any version *should* work, but use the
  newest version just in case)
* [NetworkX](https://networkx.github.io/)

Usage
===
To run FAVITES, you can use [run_favites.py](run_favites.py). You can print out
a help message listing the arguments using ``run_favites.py -h`` or
``run_favites.py --help``.

We have also included a small example contact network that you can use to test
FAVITES. Below is an example in which we run FAVITES on
[test/example_contact_network.txt](test/example_contact_network.txt)
using defaults for everything possible, using the
[EndCriteria_Transmissions](EndCriteria_Transmissions.py) module (ending
after 2 transmission events), and using a fixed transmission time delta of 10:

```
run_favites.py --ContactNetworkFile=test/example_contact_network.txt --EndCriteriaModule=Transmissions --EndTransmissions=2 --FixedTransmissionTimeDelta=10
```

General Workflow
===
1. The **[Driver](Driver.py)** module receives as input the Contact Network (in
    the form of an instance of the **[ContactNetwork](ContactNetwork.py)**
    module)
2. The **[Driver](Driver.py)** module then orchestrates the simulation process:
    1. The **[Driver](Driver.py)** module initializes the Transmission Network:
        * The **[Driver](Driver.py)** calls the
          **[SeedSelection](SeedSelection.py)** module to choose which nodes in
          the **[ContactNetwork](ContactNetwork.py)** object to be initially
          infected
        * Then, for each of these "seed" nodes, the **[Driver](Driver.py)**
          module calls the **[SeedSequence](SeedSequence.py)** module to
          generate initial infection sequence(s) and infection time for each
          seed node
        * Then, for each "seed" node, the **[Driver](Driver.py)** module calls
          the **[NodeEvolution](NodeEvolution.py)** module, which simulates the
          evolution (phylogeny and sequence) for the node given its seed
          sequence(s)
    2. The **[Driver](Driver.py)** module then repeatedly creates transmission
       events until the ending criteria in the **[EndCriteria](EndCriteria.py)**
       module are reached:
        * The **[Driver](Driver.py)** module calls the
          **[TransmissionNodeSample](TransmissionNodeSample.py)** module to
          choose two nodes to be involved in a transmission event
        * The **[Driver](Driver.py)** module calls the
          **[TransmissionTimeSample](TransmissionTimeSample.py)** module to
          choose the time of the transmission event
        * The **[Driver](Driver.py)** module calls the
          **[NodeEvolution](NodeEvolution.py)** module on the source node to
          ensure the source node is evolved until the transmission time
        * The **[Driver](Driver.py)** module calls the
          **[SourceSample](SourceSample.py)** module on the source node, passing
          in the time of transmission, and the
          **[SourceSample](SourceSample.py)** module will choose which edge(s)
          of the source node's phylogenetic tree to transmit (and thus which
          sequence(s))
    3. Once the transmission iterations have completed, the
       **[Driver](Driver.py)** module outputs the full Transmission Network, the
       full phylogenetic tree(s), the full population size profile, and the full
       sequence data (i.e., the full simulation output)
3. The **[PostValidation](PostValidation.py)** module then takes in the full
   simulation output provided by the **[Driver](Driver.py)** module and computes
   a validity score (i.e., how well the output matches what we would expect).  
4. The **[Driver](Driver.py)** module then takes in the full error-free
   simulation output and introduces real data artifacts:
    1. The **[Driver](Driver.py)** module first calls the
       **[NodeSample](NodeSample.py)** module, which subsamples the nodes in the
       Transmission Network (to simulate imperfect epidemiological efforts)
    2. The **[Driver](Driver.py)** module then calls the **SequencingError**
       module (passing in the output of the
       **[NodeSampleError](NodeSampleError.py)** module), which simulates
       sequencing imperfections (sequence subsampling per individual, sequencing
       error, post-processing, consensus, ambiguity, etc.)

Contact Network Input Format
===
For robustness to future development, we designed a file format similar to an
edge list that must be used for the input Contact Network. The first portion of
the file is a list of nodes, and the second portion is a list of edges.
* "Node" lines have three tab-delimited sections:
    1. NODE (i.e., just the string `NODE`)
    2. This node's label
    3. Attributes of this node as comma-separated values, or a period (i.e.,
       `'.'`) if this node has no attributes
* "Edge" lines have five tab-delimited sections:
    1. EDGE (i.e., just the string `EDGE`)
    2. The label of the node from which this edge leaves
    3. The label of the node to which this edge goes
    4. Attributes of this edge as comma-separated values, or a period (i.e.,
       `'.'`) if this edge has no attributes
    5. `d` (directed) or `u` (undirected) to denote whether or not this edge
       is directed (i.e., `u -> v` vs. `u <-> v`)
* Lines beginning with the pound symbol (i.e., `'#'`) and empty lines are ignored
Below is an example of this file format. Note that `<TAB>` is referring to a
single tab character (i.e., `'\t'`).
    ```bash
    #NODE<TAB>label<TAB>attributes (csv or .)
    #EDGE<TAB>u<TAB>v<TAB>attributes (csv or .)<TAB>(d)irected or (u)ndirected

    NODE<TAB>Bill<TAB>USA,Mexico
    NODE<TAB>Eric<TAB>USA
    NODE<TAB>Curt<TAB>.
    EDGE<TAB>Bill<TAB>Eric<TAB>.<TAB>d
    EDGE<TAB>Curt<TAB>Eric<TAB>Friends<TAB>u
    ```

Module Implementations
===
* **[ContactNetwork](ContactNetwork.py)**
    * [ContactNetwork_NetworkX](ContactNetwork_NetworkX.py)
        * Implements the [ContactNetwork](ContactNetwork.py) module using
          the [NetworkX](https://networkx.github.io/) Python package
        * Uses the [ContactNetworkEdge_NetworkX](ContactNetworkEdge_NetworkX.py)
          implementation of the [ContactNetworkEdge](ConContactNetworkEdge.py)
          module
        * Uses the [ContactNetworkNode_NetworkX](ContactNetworkNode_NetworkX.py)
          implementation of the [ContactNetworkNode](ConContactNetworkNode.py)
          module
        * Requires [NetworkX](https://networkx.github.io/)
* **[ContactNetworkEdge](ContactNetworkEdge.py)**
    * [ContactNetworkEdge_NetworkX](ContactNetworkEdge_NetworkX.py)
        * Implements the [ContactNetworkEdge](ContactNetworkEdge.py) module
          using the [NetworkX](https://networkx.github.io/) Python package
        * Requires [NetworkX](https://networkx.github.io/)
* **[ContactNetworkNode](ContactNetworkNode.py)**
    * [ContactNetworkNode_NetworkX](ContactNetworkNode_NetworkX.py)
        * Implements the [ContactNetworkNode](ContactNetworkNode.py) module
          using the [NetworkX](https://networkx.github.io/) Python package
        * Requires [NetworkX](https://networkx.github.io/)
* **[Driver](Driver.py)**
    * [Driver_Default](Driver_Default.py)
        * The default FAVITES driver
        * No additional dependencies
* **[EndCriteria](EndCriteria.py)**
    * [EndCriteria_FirstTimeTransmission](EndCriteria_FirstTimeTransmission.py)
        * The user can specify both an end time *and* a number of transmissions
          as ending criteria, and the first to be reached will end the
          simulation
        * No additional dependencies
    * [EndCriteria_Time](EndCriteria_Time.py)
        * The user can specify an end time, and the simulation will end when the
          time is reached
        * No additional dependencies
    * [EndCriteria_Transmissions](EndCriteria_Transmissions.py)
        * The user can specify an ending number of transmissions, and the
          simulation will end when the number of transmissions is reached
        * No additional dependencies
* **[NodeEvolution](NodeEvolution.py)**
    * [NodeEvolution_Dummy](NodeEvolution_Dummy.py)
        * Dummy implementation that will be removed once a legitimate
          implementation is created
        * No additional dependencies
* **[NodeSample](NodeSample.py)**
    * [NodeSample_Perfect](NodeSample_Perfect.py)
        * Returns the complete transmission network (i.e., assumes perfect
          epidemiological efforts in sampling the transmission network)
        * No additional dependencies
* **[PostValidation](PostValidation.py)**
    * [PostValidation_Dummy](PostValidation_Dummy.py)
        * Dummy implementation that will be removed once a legitimate
          implementation is created
        * No additional dependencies
* **[SeedSelection](SeedSelection.py)**
    * [SeedSelection_Random](SeedSelection_Random.py)
        * Seed nodes are selected from the set of all nodes in the Contact
          Network with equal probability
        * No additional dependencies
* **[SeedSequence](SeedSequence.py)**
    * [SeedSequence_Random](SeedSequence_Random.py)
        * Seed sequences are randomly generated from the DNA alphabet with equal
          probability for each nucleotide
        * No additional dependencies
* **[SourceSample](SourceSample.py)**
    * [SourceSample_Dummy](SourceSample_Dummy.py)
        * Dummy implementation that will be removed once a legitimate
          implementation is created
        * No additional dependencies
* **[TransmissionNodeSample](TransmissionNodeSample.py)**
    * [TransmissionNodeSample_Random](TransmissionNodeSample_Random.py)
        * For each transmission, the source node is selected from the set of all
          infected nodes in the Contact Network with equal probability
        * No additional dependencies
* **[TransmissionTimeSample](TransmissionTimeSample.py)**
    * [TransmissionTimeSample_Fixed](TransmissionTimeSample_Fixed.py)
        * Each transmission occurs a fixed time delta after the previous
          transmission
        * No additional dependencies
* **[Tree](Tree.py)**
    * [Tree_DendroPy](Tree_DendroPy.py)
        * Implements the [Tree](Tree.py) module using the
          [DendroPy](http://www.dendropy.org/) Python package
        * Requires [DendroPy](http://www.dendropy.org/) (any version *should*
          work, but use the newest version just in case)