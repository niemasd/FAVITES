#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from ContactNetworkNode import ContactNetworkNode

class ContactNetworkNode_PANGEA(ContactNetworkNode):
    def init():
        pass

    def __init__(self, cn, name, num):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __le__(self, other):
        return self.name <= other.name

    def __ge__(self, other):
        return self.name >= other.name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_attribute(self):
        return dict()

    def get_contact_network(self):
        return None

    def get_first_infection_time(self):
        return None

    def get_infections(self):
        return []

    def num_infections(self):
        return None

    def infect(self, time, virus):
        pass

    def is_infected(self):
        return True

    def add_virus(self, virus):
        pass

    def remove_virus(self, virus):
        pass

    def viruses(self):
        yield None

    def uninfect(self):
        pass

if __name__ == '__main__':
    pass