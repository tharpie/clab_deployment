import sys
import os
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


class InventoryHost(object):
    def __init__(self, name):
        self.name = name
        self.ordered_groups = dict()
        self.variables = dict()
        self.merged_vars = dict()

    def groups(self):
        groups = list()
        for k,v in sorted(self.ordered_groups.items()):
            groups.append(v)
        return(groups)  

class InventoryHostLibrary(object):
    """Test library for testing InventoryGroup logic.

    Interacts with InventoryGroup object using its method(s).
    """

    def __init__(self):
        self._group = None

    def create_valid_group(self, name):
        self._group = clab_inventory.InventoryGroup(name)
    
    def create_invalid_group(self, name):
        try:
            self._group = clab_inventory.InventoryGroup(name)
        except Exception as e:
            return(str(e))
        else:
            raise AssertionError(f'creating a group with {name} should have caused an error but did not')

    def set_children(self, children):
        for child in children.split():
            self._group._add_child(child)

    def set_hosts(self, hosts):
        for host in hosts.split():
            self._group._add_host(host)

    def name_should_be(self, expected):
        if self._group.name != expected:
            raise AssertionError(f'{self._group.name} != {expected}')

    def children_should_be(self, expected):
        children = ','.join(self._group.children())
        if expected != children:
            raise AssertionError(f'{expected} != {children}')

    def hosts_should_be(self, expected):
        hosts = ','.join(self._group.hosts())
        if expected != hosts:
            raise AssertionError(f'{expected} != {hosts}')

   
    
