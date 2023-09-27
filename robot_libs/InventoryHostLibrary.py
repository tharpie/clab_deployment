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

    def set_variables(self, variables, var_type):
        if var_type == 'file_name':
            variables = os.path.realpath(f'{os.getcwd()}/{variables}')
        self._host._load_variables(variables, var_type)

    def merge_variables(self, update_vars):
        self._host._merge_vars(update_vars)

    def name_should_be(self, expected):
        if self._host.name != expected:
            raise AssertionError(f'{self._host.name} != {expected}')

    def groups_should_be(self, expected):
        e = expected
        g = self._host.groups()
        if e != g:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(g)}')

    def variables_should_be(self, expected):
        e = expected
        v = self._host.variables
        if e != v:
            diff = deepdiff.DeepDiff(e,dict(v))
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')

    def private_variables_should_be(self, expected):
        e = expected
        v = self._host._vars
        if e != v:
            diff = deepdiff.DeepDiff(e,dict(v))
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')
