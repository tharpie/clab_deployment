import sys
import os
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory

TEST_GROUP1 = {}

class InventoryGroupLibrary(object):
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
    
    def name_should_be(self, expected):
        if self._group.name != expected:
            raise AssertionError(f'{self._group.name} != {expected}')

    def children_should_be(self, expected):
        children = ','.join(self._group.children())
        if expected != children:
            raise AssertionError(f'{expected} != {children}')


class InventoryGroup(object):
    def __init__(self, name):
        self.name = name
        if not self._is_valid():
            raise Exception(f'{name} has invalid InventoryGroup name')

        self.set_children = set()
        self.set_hosts = set()
        self.hosts = self._hosts()
        self.children = self._children()
        self.variables = dict()
        self.merged_vars = dict()

    def _is_valid(self):
        return(is_name_valid(self.name))

    def _add_child(self, child):
        self.set_children.add(child)
        return()
    
    def _add_host(self, host):
        self.set_hosts.add(host)
        return()
    
    def _hosts(self):
        return(list(sorted(self.set_hosts)))

    def _children(self):
        return(list(sorted(self.set_children)))