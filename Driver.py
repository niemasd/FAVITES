#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import argparse                           # to parse user arguments
from ContactNetwork import ContactNetwork # ContactNetwork module abstract class

def printMessage():
    print("/---------------------------------------------------------------------\\")
    print("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |")
    print("|                        Moshiri & Mirarab 2016                       |")
    print("\\---------------------------------------------------------------------/")

def parseArgs():
    '''
    Parse user arguments

    Returns
    -------
    user_input : list of user inputs
        * ``user_input['contact_network']'': Input contact network (edge list)

    '''

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ContactNetworkFile', default='stdin',
        help="Input contact network ('stdin' for standard input)")
    parser.add_argument('--ContactNetworkModule', default='NetworkX',
        help='ContactNetwork module implementation')
    args = parser.parse_args()

    # import modules
    print("=== Modules ===")

    # import ContactNetwork module
    print("ContactNetwork Module: ", end='')
    if args.ContactNetworkModule == 'NetworkX':
        global module_ContactNetwork
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
        assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
        print("NetworkX")

    print()

    # read input data
    print("=== Input Data ===")
    user_input = {}

    # read in Contact Network
    print("Reading contact network from: ", end='')
    user_input['contact_network'] = []
    if args.ContactNetworkFile == 'stdin':
        import sys
        user_input['contact_network'] = [i.strip() for i in sys.stdin if len(i.strip()) > 0]
        print('standard input')
    else:
        user_input['contact_network'] = open(args.ContactNetworkFile).readlines()
        print(args.ContactNetworkFile)

    # return input data
    return user_input

if __name__ == "__main__":
    '''
    Simulation driver
    '''

    # print author message
    printMessage()
    print()

    # parse user arguments
    user_input = parseArgs()

    # create ContactNetwork object from input contact network edge list
    contact_network = module_ContactNetwork(user_input['contact_network'])