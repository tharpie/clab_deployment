import sys
import os
import json
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


class InventoryHostLibrary(object):
    """Test library for testing InventoryHost logic.

    Interacts with InventoryHost object using its method(s).
    """
    def __init__(self):
        self._host = None

    def create_valid_host(self, name):
        self._host = clab_inventory.InventoryHost(name)
    
    def set_group(self, group):
        if type(group) == list:
            self._host._add_groups(group)
        else:
            self._host._add_group(group)

    def set_variables(self, input, input_type):
        self._host._load_variables(input, input_type)

    def merge_variables(self, update_vars):
        self._host._merge_vars(update_vars)

    def name_should_be(self, expected):
        self.expectation(self._host.name, expected)

    def groups_should_be(self, expected):
        e = expected
        g = self._host.groups()
        self.expectation(g, e)

    def variables_should_be(self, expected):
        e = expected
        v = self._host.variables
        self.expectation(v, e)

    def private_variables_should_be(self, expected):
        e = expected
        v = self._host._vars
        self.expectation(v, e)

    def expectation(self, a, e):
        if e != a:
            diff = deepdiff.DeepDiff(a, e, verbose_level=2)
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')
