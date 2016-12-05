**FAVITES** (FrAmework for VIral Transmission and Evolution Simulation) is a robust modular framework for the simultaneous simulation of a transmission network and viral evolution, as well as simulation of sampling imperfections of the transmission network and of the sequencing process. The framework is robust in that the simulation process has been broken down into a series of interactions between abstract module classes, and the user can simply plug in each desired module implementation (or implement one from scratch) to customize any stage of the simulation process.

For more information, including installation information, requirements, etc., be
sure to read the [FAVITES Wiki](../../wiki)

## Usage
To run FAVITES, you can use [run_favites.py](run_favites.py). You can print out
a help message listing the arguments using ``run_favites.py -h`` or
``run_favites.py --help``.

We have also included a small example contact network that you can use to test
FAVITES. Below is an example in which we run FAVITES on
[test/example_contact_network.txt](test/example_contact_network.txt)
using defaults for everything possible, using the
[EndCriteria_Transmissions](../../wiki/Module:-EndCriteria) module (ending
after 2 transmission events), and using a fixed transmission time delta of 10:

```
run_favites.py --ContactNetworkFile=test/example_contact_network.txt --EndCriteriaModule=Transmissions --EndTransmissions=2 --FixedTransmissionTimeDelta=10