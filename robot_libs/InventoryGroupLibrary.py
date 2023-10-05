import sys
import os
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


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

    def set_children(self, child):
        if type(child) == list:
            self._group._add_children(child)
        else:
            self._group._add_child(child)

    def set_host(self, host):
        if type(host) == list:
            self._group._add_hosts(host)
        else:
            self._group._add_host(host)

    def set_variables(self, input, input_type):
        self._group._load_variables(input, input_type)

    def merge_variables(self, update_vars):
        self._group._merge_vars(update_vars)

    def name_should_be(self, expected):
        self.expectation(self._group.name, expected)

    def children_should_be(self, expected):
        e = expected
        c = self._group.children()
        self.expectation(c, e)

    def hosts_should_be(self, expected):
        e = expected
        h = self._group.hosts()
        self.expectation(h, e)

    def variables_should_be(self, expected):
        e = expected
        v = self._group.variables
        self.expectation(v, e)

    def expectation(self, a, e):
        if e != a:
            diff = deepdiff.DeepDiff(a, e, verbose_level=2)
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')
