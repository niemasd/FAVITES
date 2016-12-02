#FAVITES - FrAmework for VIral Transmission and Evolution Simulation

Architecture
===

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
    5. d (for directed) or e (for undirected) to denote whether or not this edge
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