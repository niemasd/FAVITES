#FAVITES - FrAmework for VIral Transmission and Evolution Simulation

GENERAL WORKFLOW
===
* The **Driver** module receives as input the Interaction Network
* The **Driver** module then orchestrates the simulation process:
    * The **Driver** module initializes the Transmission Network using the **SeedSelection** module
        * The **SeedSelection** module chooses which nodes in the Interaction Network to be initially infected
        * For each of these "seed" nodes, the **SeedSelection** module calls the **SeedSequence** module to generate initial infection sequence(s) and infection time for the node
        * Then, for each "seed" node, the **SeedSelection** module calls the **NodeEvolution** module, which simulates the evolution (phylogeny + sequence) for the node given its seed sequence(s)
    * The **Driver** module then repeatedly calls the **TransmissionSample** module to choose two nodes to be involved in a transmission event as well as the time of the transmission:
        * The **TransmissionSample** module calls the **SourceSample** module on the source node, passing in the time of transmission, and the **SourceSample** module will choose which edges of the source node's phylogenetic tree to transmit (and thus sequences)
        * The **TransmissionSample** module calls the **NodeEvolution** module on the destination node, feeding in the sequences obtained from the **SourceSample** module
    * Once the transmission iterations have completed, the **Driver** module outputs the full Transmission Network, the full phylogenetic tree(s), the full population size profile, and the full sequence data (i.e., the full simulation output)
* The **PostValidation** module then takes in the full simulation output provided by the **Driver** module and computes a validity score (i.e., how well the output matches what we would expect)
* The **ErrorSimulation** module then takes in the full simulation output provided by the **Driver** module and introduces realistic error:
    * The **ErrorSimulation** module first calls the **NodeSampleError** module, which subsamples the nodes in the Transmission Network (to simulate imperfect epidemiological efforts)
    * The **ErrorSimulation** module then calls the **SequencingError** module (passing in the output of the **NodeSampleError** module), which simulates sequencing imperfections (sequence subsampling, sequencing error, post-processing, etc.)