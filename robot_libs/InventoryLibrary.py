import sys
import os
import json
import deepdiff
sys.path.append(f'{os.getcwd()}/pylibs')
import clab_inventory


class InventoryLibrary(object):
    """Test library for testing Inventory logic.

    Interacts with Inventory object using its method(s).
    """
    def __init__(self):
        self._inventory = None

    def create_valid_inventory(self, base, base_type):
        self._inventory = clab_inventory.Inventory(base, base_type)
    
    def merge_variables(self, update_vars):
        self._inventory._merge_vars(update_vars)

    def load_inventory(self):
        self._inventory.load()

    def groups_should_be(self, expected):
        e = expected
        g = self._inventory.groups()
        if e != g:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(g)}')

    def hosts_should_be(self, expected):
        e = expected
        h = self._inventory.hosts()
        if e != h:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(h)}')

    def children_should_be(self, parent_name, expected):
        e = expected
        c = self._inventory.group(parent_name).children()
        if e != c:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(c)}')

    def parent_should_be(self, group_name, expected):
        e = expected
        p = self._inventory.group(group_name).parent
        if e != p:
            raise AssertionError(f'EXPECTED={str(e)}\n!=\nACTUAL={str(p)}')

    def private_variables_should_be(self, expected):
        e = expected
        v = self._inventory._vars
        if e != v:
            diff = deepdiff.DeepDiff(e,dict(v))
            raise AssertionError(f'Diff=\n{diff.pretty()}\n')

