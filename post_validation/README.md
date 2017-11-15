This directory contains a series of tools that can be used to post-validate the simulation output produced by FAVITES.

* **[compare_trees.py](compare_trees.py):** Compare a given simulated tree against a given reference tree
    * Compare distributions of all branch lengths, internal branch lengths, terminal branch lengths, and root-to-tip distances
    * Usage: `compare_trees.py [-h] -r REF -s SIM [-n NW_DISTANCE]`
        * `REF`: Reference tree (Newick format)
        * `SIM`: Simulated tree (Newick format)
        * `NW_DISTANCE`: Path to `nw_distance` executable (if not in `PATH`)
* **[sequence_score_profile_HMM.py](sequence_score_profile_HMM.py):** Score a given sequence dataset against a given profile HMM
    * Usage: sequence_score_profile_HMM.py [-h] -H HMM -s SEQ [-q] [-a HMMSCAN]
        * `HMM`: Profile HMM (HMMER format)
        * `SEQ`: Sequence file
        * `-q`: Input file is FASTQ (not FASTA)
        * `HMMSCAN`: Path to `HMMSCAN` executable (if not in `PATH`)