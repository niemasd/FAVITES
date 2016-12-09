**FAVITES** (FrAmework for VIral Transmission and Evolution Simulation) is a robust modular framework for the simultaneous simulation of a transmission network and viral evolution, as well as simulation of sampling imperfections of the transmission network and of the sequencing process. The framework is robust in that the simulation process has been broken down into a series of interactions between abstract module classes, and the user can simply plug in each desired module implementation (or implement one from scratch) to customize any stage of the simulation process.

For more information, including installation information, requirements, etc., be
sure to read the [FAVITES Wiki](../../wiki)

## Usage
To run FAVITES, you can use [run_favites.py](run_favites.py). You can print out
a help message listing the arguments using ``run_favites.py -h`` or
``run_favites.py --help``.

We have also included a small example configuration file and contact network in
[example](example).