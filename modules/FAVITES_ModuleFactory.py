#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global FAVITES module-related variables.
'''
from sys import path
from importlib import import_module

HIDDEN_MODULES = {'ContactNetworkEdge','ContactNetworkNode'}

def favites_import(name):
    '''
    Import module from string name.
    '''
    return getattr(import_module(name),name)

def read_config(config, verbose):
    '''
    Read user configuration. Call after init.

    Parameters
    ----------
    config : dictionary
        User configuration
    '''
    assert 'modules' in globals(), "You must call init() before calling read_config()!"

    # import module implementations
    reqs = {}
    for module in sorted(module_implementations.keys()):
        if module in HIDDEN_MODULES:
            continue
        assert module in config, "Module %r is not in the configuration file!" % module
        assert config[module] in module_implementations[module], "%r is not a valid %r!" % (config[module], module)
        modules[module] = module_implementations[module][config[module]]['class']
        modules[module]() # instantiate to force check of abstract methods
        for req in sorted(module_implementations[module][config[module]]['req']):
            assert req in config, "Parameter %r of %s_%s module is not in the configuration file!" % (req, module, config[module])
            reqs[req] = config[req]
    GC.init(reqs)
    GC.VERBOSE = verbose

def init(mod_dir):
    '''
    Initialize global access variables.

    Parameters
    ----------
    mod_dir : string
        String representing the path to the modules directory
    '''

    # get modules directory
    global dir_modules
    dir_modules = mod_dir
    path.append(mod_dir)

    # import global context
    global GC
    import FAVITES_GlobalContext as GC

    # load list of all module implementations
    global module_implementations
    module_implementations = eval(open(dir_modules + '/FAVITES_ModuleList.json').read())

    # load abstract module classes
    global module_abstract_classes
    module_abstract_classes = {}
    for module in module_implementations:
        module_abstract_classes[module] = favites_import(module)

    # validate all module implementations
    for module in module_implementations:
        for implementation in module_implementations[module]:
            module_implementations[module][implementation]['class'] = favites_import(module + '_' + implementation)
            assert issubclass(module_implementations[module][implementation]['class'], module_abstract_classes[module]), "Class " + module + "_" + implementation + " is not a valid " + module

    # dictionary to store which implementation of each module was chosen
    global modules
    modules = {}

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    init()