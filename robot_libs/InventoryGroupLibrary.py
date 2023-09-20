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

    def name_should_be(self, expected):
        if self._group.name != expected:
            raise AssertionError(f'{self._group.name} != {expected}')

    def set_variables(self, variables, var_type):
        if var_type == 'file_name':
            variables = os.path.realpath(f'{os.getcwd()}/{variables}')
        self._group._load_variables(variables, var_type)

    def merge_variables(self, update_vars):
        self._group._merge_vars(update_vars)
    
    def children_should_be(self, expected):
        e = expected
        c = sorted(list(self._group.children()))
        if e != c:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(c)}')

    def hosts_should_be(self, expected):
        e = expected
        h = sorted(list(self._group.hosts()))
        if e != h:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(h)}')

    def variables_should_be(self, expected):
        e = expected
        v = self._group.variables
        if e != v:
            diff = deepdiff.DeepDiff(e,dict(v))
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')

