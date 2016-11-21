#FAVITES - FrAmework for VIral Transmission and Evolution Simulation

Architecture
===

General Workflow
===
* The **Driver** module receives as input the Contact Network (in the form of an
  instance of the **ContactNetwork** module)
* The **Driver** module then orchestrates the simulation process:
    1. The **Driver** module initializes the Transmission Network:
        * The **Driver** calls the **SeedSelection** module to choose 
        which nodes in the **ContactNetwork** object to be initially infected
        * Then, for each of these "seed" nodes, the **Driver** module calls the
          **SeedSequence** module to generate initial infection sequence(s) and
          infection time for each seed node
        * Then, for each "seed" node, the **Driver** module calls the
          **NodeEvolution** module, which simulates the evolution (phylogeny and
          sequence) for the node given its seed sequence(s)
    * The **Driver** module then repeatedly creates transmission events:
        * The **Driver** module calls the **TransmissionSample**
           module to choose two nodes to be involved in a transmission event as well
           as the time of the transmission:
        * The **Driver** module calls the **SourceSample** module on
          the source node, passing in the time of transmission, and the
          **SourceSample** module will choose which edges of the source node's
          phylogenetic tree to transmit (and thus sequences)
        * The **Driver** module calls the **NodeEvolution** module
          on the destination node, feeding in the sequences obtained from the
          **SourceSample** module as the initial sequence
    * Once the transmission iterations have completed, the **Driver** module
      outputs the full Transmission Network, the full phylogenetic tree(s), the
      full population size profile, and the full sequence data (i.e., the full
      simulation output)
* The **PostValidation** module then takes in the full simulation output
  provided by the **Driver** module and computes a validity score (i.e., how
  well the output matches what we would expect).  
* The **Driver** module then takes in the full error-free simulation output
 and introduces real data artifacts:
    * The **Driver** module first calls the **NodeSample** module,
      which subsamples the nodes in the Transmission Network (to simulate
      imperfect epidemiological efforts)
    * The **Driver** module then calls the **SequencingError** module
      (passing in the output of the **NodeSampleError** module), which simulates
      sequencing imperfections (sequence subsampling per individual,
      sequencing error, post-processing, consensus, ambiguity, etc.)
