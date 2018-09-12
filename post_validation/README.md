This directory contains a series of tools that can be used to post-validate the simulation output produced by FAVITES.

* **[compare_contact_networks.py](compare_contact_networks.py):** Compare a given simulated contact network against a reference contact network
    * Compare distribution of node degrees
    * Usage: `compare_contact_networks.py [-h] -r REF -s SIM`
        * `REF`: Reference contact network (FAVITES format)
        * `SIM`: Simulated contact network (FAVITES format)

* **[compare_trees.py](compare_trees.py):** Compare a given simulated tree against a given reference tree
    * Compare distributions of all branch lengths, internal branch lengths, terminal branch lengths, and root-to-tip distances
    * Usage: `compare_trees.py [-h] -r REF -s SIM [-n NW_DISTANCE]`
        * `REF`: Reference tree (Newick format)
        * `SIM`: Simulated tree (Newick format)
        * `NW_DISTANCE`: Path to `nw_distance` executable (if not in `PATH`)

* **[distribution_distance.py](distribution_distance.py):** Compute a distance between the distributions of two given samples
    * Input distribution samples should contain a single sample per line
    * Usage: `distribution_distance.py [-h] -1 DIST1 -2 DIST2 [-d DISTANCE] [-n NUM_POINTS]`
        * `DIST1`: File containing samples from distribution 1
        * `DIST2`: File containing samples from distribution 2
        * `DISTANCE`: The distance to compute
            * `jsd`: Jensen-Shannon Divergence
            * `jsm`: Jensen-Shannon Metric
            * `ks`: Kolmogorov-Smirnov Distance (returns a (distanc, p-value) tuple)
        * `NUM_POINTS`: Number of Points when Discretizing PDF (used in jsd, jsm)

* **[sequence_score_profile_HMM.py](sequence_score_profile_HMM.py):** Score a given sequence dataset against a given profile HMM
    * Usage: `sequence_score_profile_HMM.py [-h] -H HMM -s SEQ [-q] [-a HMMSEARCH]`
        * `HMM`: Profile HMM (HMMER format)
        * `SEQ`: Sequence file
        * `-q`: Input file is FASTQ (not FASTA)
        * `HMMSEARCH`: Path to `hmmsearch` executable (if not in `PATH`)
