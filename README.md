#FAVITES - FrAmework for VIral Transmission and Evolution Simulation

Architecture
===

General Workflow
===
1. The **[Driver](Driver.py)** module receives as input the Contact Network (in the form of
    an instance of the **[ContactNetwork](ContactNetwork.py)** module)
2. The **[Driver](Driver.py)** module then orchestrates the simulation process:
    1. The **[Driver](Driver.py)** module initializes the Transmission Network:
        * The **[Driver](Driver.py)** calls the **SeedSelection** module to choose which
          nodes in the **ContactNetwork** object to be initially infected
        * Then, for each of these "seed" nodes, the **[Driver](Driver.py)** module calls the
          **SeedSequence** module to generate initial infection sequence(s) and
          infection time for each seed node
        * Then, for each "seed" node, the **[Driver](Driver.py)** module calls the
          **NodeEvolution** module, which simulates the evolution (phylogeny and
          sequence) for the node given its seed sequence(s)
    2. The **[Driver](Driver.py)** module then repeatedly creates transmission events:
        * The **[Driver](Driver.py)** module calls the **TransmissionSample** module to
          choose two nodes to be involved in a transmission event as well as the
          time of the transmission:
        * The **[Driver](Driver.py)** module calls the **SourceSample** module on the source
          node, passing in the time of transmission, and the **SourceSample**
          module will choose which edge(s) of the source node's phylogenetic
          tree to transmit (and thus which sequence(s))
        * The **[Driver](Driver.py)** module calls the **NodeEvolution** module on the
          destination node, feeding in the sequences obtained from the
          **SourceSample** module as the initial sequence
    3. Once the transmission iterations have completed, the **[Driver](Driver.py)** module
       outputs the full Transmission Network, the full phylogenetic tree(s), the
       full population size profile, and the full sequence data (i.e., the full
       simulation output)
3. The **PostValidation** module then takes in the full simulation output
   provided by the **[Driver](Driver.py)** module and computes a validity score (i.e., how
   well the output matches what we would expect).  
4. The **[Driver](Driver.py)** module then takes in the full error-free simulation output
   and introduces real data artifacts:
    1. The **[Driver](Driver.py)** module first calls the **NodeSample** module, which
       subsamples the nodes in the Transmission Network (to simulate imperfect
       epidemiological efforts)
    2. The **[Driver](Driver.py)** module then calls the **SequencingError** module (passing
       in the output of the **NodeSampleError** module), which simulates
       sequencing imperfections (sequence subsampling per individual, sequencing
       error, post-processing, consensus, ambiguity, etc.)
