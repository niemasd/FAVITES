This directory contains a series of tools that can be used to help users with various miscellaneous tasks.

* **[clean_labels.py](clean_labels.py):** For each read of the given sequence file or each leaf of a given phylogenetic tree, remove everything from the label except for the contact network individual's name
    * Usage: `clean_sequence_headers.py [-h] [-i INPUT] [-o OUTPUT]`
        * `INPUT`: Input FASTQ/FASTA/Newick File (default: standard input)
        * `OUTPUT`: Input FASTQ/FASTA/Newick File (default: standard output)
            * The output format (FASTA/FASTQ/Newick) matches the input format and is detected automatically
            * If you wish to convert a FASTQ file to FASTA, refer to [fastq2fasta.py](https://github.com/niemasd/tools/blob/master/fastq2fasta.py) in my [tools repository](https://github.com/niemasd/tools)

* **[cluster_previous_time.py](cluster_previous_time.py):** Given a clustering from the simulation end time, a FAVITES-format transmission network, and a time, remove individuals who were not infected at the given time and output the resulting clusters.
    * Usage: `cluster_previous_time.py [-h] -c CLUSTERING -tn TRANSMISSIONS -t TIME [-o OUTPUT]`
        * `CLUSTERING`: Input clustering file (Cluster Picker format)
        * `TRANSMISSIONS`: Input transmission network (FAVITES format)
        * `TIME`: Time to remove all individuals infected after
        * `OUTPUT`: Output file (default: standard output)

* **[cn_adjacency_matrix_to_favites.py](cn_adjacency_matrix_to_favites.py):** Convert a given contact network from a binary adjacency matrix to the FAVITES format
    * Usage: `cn_adjacency_matrix_to_favites.py [-h] -i INPUT [-o OUTPUT] [-d DELIM]`
        * `INPUT`: Input contact network file (binary adjacency matrix)
        * `OUT`: Output contact network file (FAVITES format) (default: standard output)
        * `DELIM`: Column delimiter of input binary adjacency matrix (default: empty string)

* **[degree_stats.py](degree_stats.py):** Given a contact or transmission network, compute various statistics of the node degree distribution
    * Usage: `degree_stats.py [-h] -i INPUT`
        * `INPUT`: Input contact or transmission network file (FAVITES format)

* **[FAVITES2GEXF.py](FAVITES2GEXF.py):** Convert a FAVITES contact network and transmission network to the GEXF format
    * Usage: `FAVITES2GEXF.py [-h] -c CONTACT_NETWORK -t TRANSMISSION_NETWORK [-o OUTPUT]`
        * `CONTACT_NETWORK`: FAVITES-format contact network
        * `TRANSMISSION_NETWORK`: FAVITES-format transmission network
        * `OUTPUT` Output file (default: standard output)

* **[label_internal_nodes.py](label_internal_nodes.py):** Label the internal nodes of a simulated tree with the corresponding infected individual
    * Usage: `label_internal_nodes.py [-h] -tn TRANSMISSION_NETWORK -tt TREE_TIME [-tm TREE_MUTATION] -ot OUTPUT_TIME [-om OUTPUT_MUTATION]`
        * `TRANSMISSION_NETWORK`: FAVITES-format transmission network
        * `TREE_TIME`: Simulated tree in unit of time
        * `TREE_MUTATION`: Simulated tree in unit of expected number of per-site mutations
        * `OUTPUT_TIME`: Output labeled tree in unit of time
        * `OUTPUT_MUTATION`: Output labeled tree in unit of expected number of per-site mutations

* **[PANGEA_transmissions_to_FAVITES.py](PANGEA_transmissions_to_FAVITES.py):** Convert a PANGEA transmission network into the FAVITES edge-list format
    * Usage: `PANGEA_transmissions_to_FAVITES.py [-h] -i INPUT [-o OUTPUT]`
        * `INPUT`: Input PANGEA transmission network (.csv)
        * `OUTPUT`: Output file (default: stdout)

* **[patristic_distances.py](patristic_distances.py):** Given a phylogenetic tree, compute the pairwise distances between leaves and output the resulting distance matrix as a CSV file
    * Usage: `patristic_distances.py [-h] -t TREE [-s SCHEMA] [-o OUTPUT]`
        * `TREE`: Input tree
        * `SCHEMA`: Input tree schema (default: Newick)
        * `OUTPUT`: Output file (default: standard output)

* **[scale_tree.py](scale_tree.py):** Given a phylogenetic tree (in the Newick format), scale all branches
    * Usage: `scale_tree.py [-h] -t TREE [-o OUTPUT] -m MODE [parameters]`
        * `TREE`: Input tree
        * `OUTPUT`: Output file (default: stdout)
        * `MODE`: Scaling mode
            * Constant: `scale_tree.py -t TREE [-o OUTPUT] -m c CONSTANT`
            * Exponential: `scale_tree.py -t TREE [-o OUTPUT] -m e SCALE`
            * Gamma: `scale_tree.py -t TREE [-o OUTPUT] -m g SHAPE SCALE`
            * Log-Normal: `Log-Normal Mode Usage: scale_tree.py -t TREE [-o OUTPUT] -m ln MU SIGMA`

* **[score_clusters.py](score_clusters.py):** Score a given query clustering against a given true reference clustering
    * Usage: `score_clusters.py [-h] -q QUERY -r REFERENCE -m METRIC`
        * `QUERY`: Query clustering file (Cluster Picker format)
        * `REFERENCE`: Reference clustering file (Cluster Picker format)
        * `METRIC`: Scoring metric
            * `AMI`: Adjusted Mutual Information
            * `ARI`: Adjusted Rand Index
            * `COM`: Completeness Score
            * `FMI`: Fowlkes-Mallows Index
            * `HCV`: Compute Homogeneity, Completeness, and V-Measure simultaneously
            * `HOM`: Homogeneity Score
            * `MI`: Mutual Information
            * `NMI`: Normalized Mutual Information
            * `VM`: V-Measure

* **[tn93_to_clusters.py](tn93_to_clusters.py):** Convert tn93 output to the Cluster Picker clustering format
    * Usage: `tn93_to_clusters.py [-h] -i INPUT [-t THRESHOLD] [-o OUTPUT]`
        * `INPUT`: Input TN93 distances file
        * `THRESHOLD`: Distance threshold *t* (default: infinity)
            * Two individuals *u* and *v* are placed in a cluster together if their distance is less than or equal to *t*
        * `OUTPUT`: Output file (default: standard output)
